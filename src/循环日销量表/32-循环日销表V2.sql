/*==============================================================================
    文件名: 32-循环日销表V2.sql
    功能描述: 循环日销量表分析系统 - 版本2
    创建时间: 2024-03-21
    版本: V2.0
    
    主要功能:
    1. 动态循环获取多年份日销量数据
    2. 分析产品清单和销售数据
    3. 计算库存和销售指标
    4. 生成门店经营分析报表
    5. 统计门店经营天数和活跃度
    
    优化内容:
    - 添加详细注释和错误处理
    - 优化循环逻辑和性能
    - 增加数据验证和统计分析
    - 规范化临时表管理
    - 完善门店分类逻辑
==============================================================================*/

-- 设置会话选项
SET NOCOUNT ON;
SET ANSI_WARNINGS OFF;

BEGIN TRY
    /*==============================================================================
        第一部分: 参数设置和变量声明
    ==============================================================================*/
    
    -- 声明日期变量
    DECLARE @SDD DATETIME,       -- 开始日期
            @EDD DATETIME,       -- 结束日期
            @CURDD DATETIME,     -- 当前日期
            @CY_YYYY VARCHAR(4), -- 当前年份
            @CY_DATE VARCHAR(8); -- 当前日期字符串
    
    -- 设置分析时间范围（从2024年初到昨天）
    SET @SDD = DATEADD(dd, DATEDIFF(dd, 0, CONVERT(datetime, '2024-1-1')), 0);  -- 2024年1月1日
    SET @EDD = DATEADD(dd, DATEDIFF(dd, 0, GETDATE()-1), 0);                   -- 昨天
    SET @CURDD = DATEADD(dd, DATEDIFF(dd, 0, GETDATE()), 0);                   -- 今天
    SET @CY_DATE = CONVERT(VARCHAR(20), @SDD, 112);                            -- 格式化日期
    SET @CY_YYYY = YEAR(@SDD);                                                  -- 提取年份
    
    -- 输出参数用于调试
    SELECT 
        @CY_DATE AS 当前处理日期,
        @CY_YYYY AS 当前年份,
        @SDD AS 开始日期,
        @EDD AS 结束日期,
        @CURDD AS 当前日期,
        DATEDIFF(DAY, @SDD, @EDD) + 1 AS 分析天数;

    /*==============================================================================
        第二部分: 创建基础临时表
    ==============================================================================*/
    
    -- 清理可能存在的临时表
    DROP TABLE IF EXISTS #moutdrpt;
    DROP TABLE IF EXISTS #ddplist;
    DROP TABLE IF EXISTS #sale_data1;
    DROP TABLE IF EXISTS #sale_data11;
    DROP TABLE IF EXISTS #sales0705;
    DROP TABLE IF EXISTS #sale_data2;
    DROP TABLE IF EXISTS #stk;
    DROP TABLE IF EXISTS #stk2;
    DROP TABLE IF EXISTS #sale01;
    DROP TABLE IF EXISTS #stk01;
    DROP TABLE IF EXISTS #stores;
    DROP TABLE IF EXISTS #store2;
    DROP TABLE IF EXISTS #TS;
    DROP TABLE IF EXISTS #ts2;
    
    -- 创建门店日销量数据临时表
    CREATE TABLE #moutdrpt (
        astore VARCHAR(10),     -- 门店编码
        adate DATETIME,         -- 销售日期
        bgdgid VARCHAR(10),     -- 商品编码
        dq1 MONEY,             -- 期初数量
        dq5 MONEY,             -- 期末数量
        dt1 MONEY,             -- 期初金额
        dt5 MONEY              -- 期末金额
    );
    
    PRINT '基础临时表创建完成，开始循环获取数据...';

    /*==============================================================================
        第三部分: 循环获取多年份销售数据
    ==============================================================================*/
    
    DECLARE @SQL1 VARCHAR(MAX);
    DECLARE @RecordCount INT = 0;  -- 记录处理的数据量
    
    -- 循环处理每一天的数据（注意：湖南数据需要特殊处理）
    WHILE @SDD < @CURDD
    BEGIN
        -- 动态构建SQL语句，从对应年份和日期的表中获取数据
        SET @SQL1 = '
        IF EXISTS (SELECT 1 FROM sys.databases WHERE name = ''odsdbfq_' + @CY_YYYY + ''')
        BEGIN
            IF EXISTS (SELECT 1 FROM odsdbfq_' + @CY_YYYY + '.INFORMATION_SCHEMA.TABLES 
                      WHERE TABLE_NAME = ''moutdrpt_' + @CY_DATE + ''')
            BEGIN
                INSERT INTO #moutdrpt
                SELECT astore, adate, bgdgid, dq1, dq5, dt1, dt5 
                FROM odsdbfq_' + @CY_YYYY + '.dbo.moutdrpt_' + @CY_DATE + ' WITH (NOLOCK)
                WHERE companycode = ''hn'';  -- 注意：hn代表湖南数据
                
                SET @RecordCount = @RecordCount + @@ROWCOUNT;
            END
        END';
        
        -- 推进到下一天
        SET @SDD = DATEADD(day, +1, @SDD);
        SET @CY_YYYY = YEAR(@SDD);
        SET @CY_DATE = CONVERT(VARCHAR(20), @SDD, 112);
        
        -- 执行动态SQL
        EXEC (@SQL1);
    END;
    
    PRINT '数据循环获取完成，总共处理 ' + CAST(@RecordCount AS VARCHAR(20)) + ' 条记录';

    /*==============================================================================
        第四部分: 获取产品清单数据
    ==============================================================================*/
    
    -- 获取产品清单（注意：mydate、DQ、remark 3个字段为过滤条件）
    SELECT a.*,
           b.gid,
           scode1 AS 大类编码,
           sname1 AS 大类名称 
    INTO #ddplist 
    FROM odsdbfqbi.dbo.ddp_hn a WITH (NOLOCK)
    LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) 
        ON a.itemcode = b.code AND b.companycode = 'hn'
    WHERE mydate = '202401' 
      AND DQ = '全部';  -- 过滤条件：202401月份，全部地区
    
    PRINT '产品清单获取完成，共 ' + CAST(@@ROWCOUNT AS VARCHAR(10)) + ' 个产品';

    /*==============================================================================
        第五部分: 销售数据分析处理
    ==============================================================================*/
    
    -- 5.1 计算指定产品的销售数据（基于产品清单的销售分析）
    SELECT astore AS storegid,
           bgdgid AS 商品gid,
           SUM(DQ1 - DQ5) AS 销售数量,
           SUM(DT1 - DT5) AS 销售金额 
    INTO #sale_data1
    FROM #moutdrpt
    WHERE bgdgid IN (SELECT gid FROM #ddplist)
    GROUP BY astore, bgdgid;
    
    PRINT '指定产品销售数据分析完成';

    -- 5.2 计算所有产品的销售数据（包含0705类别特殊分析）
    SELECT astore AS storegid,
           bgdgid AS 商品gid,
           SUM(DQ1 - DQ5) AS 销售数量,
           SUM(DT1 - DT5) AS 销售金额 
    INTO #sale_data11
    FROM #moutdrpt
    GROUP BY astore, bgdgid;

    -- 5.3 分析0705类别商品销售数据（过滤销售门店）
    SELECT a.*,
           c.code AS 门店编码,
           scode2,
           syb AS 事业部 
    INTO #sales0705 
    FROM #sale_data11 a
    LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) 
        ON a.商品gid = b.gid AND b.companycode = 'hn'
    LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) 
        ON a.storegid = c.gid AND c.companycode = 'hn'
    WHERE scode2 = '0705';  -- 特定商品类别过滤
    
    -- 统计0705类别有销售的门店数
    SELECT ISNULL(d.事业部, a.事业部) AS 事业部,
           COUNT(门店编码) AS 有销售门店数 
    FROM (
        SELECT DISTINCT 门店编码, 事业部 
        FROM #sales0705 
        WHERE 销售金额 > 0 
    ) a
    LEFT JOIN odsdbfqbi.dbo.storeinf d WITH (NOLOCK) ON a.门店编码 = d.编号
    GROUP BY ISNULL(d.事业部, a.事业部);

    /*==============================================================================
        第六部分: 匹配完整销售数据信息
    ==============================================================================*/
    
    -- 关联产品清单、门店信息，生成完整销售数据
    SELECT c.shoptype AS 店型,
           syb AS 事业部,
           kfq AS 开发区,
           mentor AS 督导,
           manager AS 指导员,
           c.code AS 编号,
           大类编码,
           大类名称,
           remark AS 备注,
           DQ AS 地区,
           b.itemcode AS 商品编码,
           b.itemcn AS 商品名称,
           销售数量,
           销售金额 
    INTO #sale_data2 
    FROM #sale_data1 a
    LEFT JOIN #ddplist b ON a.商品gid = b.gid
    LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) 
        ON a.storegid = c.gid AND c.companycode = 'hn';
    
    PRINT '销售数据匹配完成';

    /*==============================================================================
        第七部分: 库存数据分析
    ==============================================================================*/
    
    -- 7.1 获取指定产品的库存数据
    SELECT a.store AS 店gid,
           a.gdgid AS 商品gid,
           b.code AS 商品编码,
           b.scode1 AS 大类编码,
           b.sname1 AS 大类名称,
           b.[name] AS 商品名称,
           c.code AS 编号,
           c.[name] AS 店名,
           shoptype AS 店型,
           syb AS 事业部,
           kfq AS 开发区,
           mentor AS 督导,
           manager AS 指导员,
           wrh,
           qty AS 库存数量,
           qty * ISNULL(whsprc, 0) AS 库存金额
    INTO #stk 
    FROM odsdbfq_basic.dbo.inv a WITH (NOLOCK)
    LEFT JOIN odsdbfq_basic.dbo.goodsz b WITH (NOLOCK) 
        ON a.gdgid = b.gid AND b.companycode = 'hn'
    LEFT JOIN odsdbfq_basic.dbo.store c WITH (NOLOCK) 
        ON a.store = c.gid AND c.CompanyCode = 'hn'
    WHERE a.companycode = 'hn' 
      AND b.scode1 IS NOT NULL 
      AND c.code <> '08' 
      AND a.gdgid IN (SELECT gid FROM #ddplist);
    
    -- 7.2 关联产品清单的备注和地区信息
    SELECT a.*, 
           b.remark AS 备注,
           b.DQ AS 地区 
    INTO #stk2 
    FROM #stk a
    LEFT JOIN #ddplist b ON a.商品编码 = b.itemcode;
    
    PRINT '库存数据分析完成';

    /*==============================================================================
        第八部分: 数据汇总统计
    ==============================================================================*/
    
    -- 8.1 按备注和编号汇总销售数据
    SELECT 备注,
           编号,
           SUM(销售数量) AS 销售数量,
           SUM(销售金额) AS 销售金额 
    INTO #sale01 
    FROM #sale_data2
    GROUP BY 编号, 备注;

    -- 8.2 按备注和编号汇总库存数据
    SELECT 备注,
           编号,
           SUM(库存数量) AS 库存数量,
           SUM(库存金额) AS 库存金额 
    INTO #stk01 
    FROM #stk2
    GROUP BY 编号, 备注;

    /*==============================================================================
        第九部分: 门店信息处理
    ==============================================================================*/
    
    -- 9.1 获取有效门店清单
    SELECT syb AS 事业部,
           kfq AS 开发区,
           mentor AS 督导,
           manager AS 指导员,
           code AS 编号,
           [name] AS 店名,
           shoptype AS 店型
    INTO #stores 
    FROM odsdbfq_basic.dbo.store WITH (NOLOCK)
    WHERE stat = '有效' AND companycode = 'hn';

    -- 9.2 交叉关联所有门店和产品备注
    SELECT b.remark AS 备注, a.* 
    INTO #store2 
    FROM #stores a
    CROSS JOIN (SELECT DISTINCT remark FROM #ddplist WHERE remark IS NOT NULL) b;

    -- 9.3 更新特定门店的事业部信息
    UPDATE #store2
    SET 事业部 = '休闲食品部' 
    WHERE 编号 IN (
        SELECT DISTINCT 编号 
        FROM odsdbfqbi.dbo.storeinf WITH (NOLOCK)
        WHERE 事业部 = '休闲食品部'
    );
    
    PRINT '门店信息处理完成';

    /*==============================================================================
        第十部分: 生成最终分析报表
    ==============================================================================*/
    
    -- 最终汇总报表：门店销售和库存综合分析
    SELECT a.事业部,
           a.开发区,
           a.督导,
           a.指导员,
           a.编号,
           a.店名,
           a.店型,
           a.备注 AS 商品,
           ISNULL(b.销售数量, 0) AS 销售数量,
           ISNULL(b.销售金额, 0) AS 销售金额,
           ISNULL(c.库存数量, 0) AS 库存数量,
           ISNULL(c.库存金额, 0) AS 库存金额,
           CASE WHEN e.门店编码 IS NOT NULL AND a.备注 = '饮料' THEN 'Y' ELSE 'N' END AS 是否开货,
           CASE WHEN ISNULL(b.销售金额, 0) <= 0 THEN 1 ELSE 0 END AS 滞动店,
           CASE WHEN ISNULL(b.销售金额, 0) <= 0 AND ISNULL(c.库存金额, 0) > 0 THEN 1 ELSE 0 END AS 有库存滞动店,
           CASE WHEN ISNULL(c.库存金额, 0) <= 0 THEN 1 ELSE 0 END AS 缺货,
           -- 计算库存周转天数（基于销售金额）
           CASE WHEN ISNULL(b.销售金额, 0) > 0 
                THEN ROUND(ISNULL(c.库存金额, 0) / (ISNULL(b.销售金额, 0) / DATEDIFF(DAY, '2024-01-01', @EDD)), 1)
                ELSE NULL END AS 库存周转天数,
           -- 计算销售占比
           CASE WHEN (SELECT SUM(销售金额) FROM #sale01 WHERE 备注 = a.备注) > 0
                THEN ROUND(ISNULL(b.销售金额, 0) * 100.0 / 
                          (SELECT SUM(销售金额) FROM #sale01 WHERE 备注 = a.备注), 2)
                ELSE 0 END AS 销售占比
    FROM #store2 a
    LEFT JOIN #sale01 b ON a.编号 = b.编号 AND a.备注 = b.备注
    LEFT JOIN #stk01 c ON a.编号 = c.编号 AND a.备注 = c.备注
    LEFT JOIN (SELECT DISTINCT 门店编码, 事业部 FROM #sales0705 WHERE 销售金额 > 0) e 
        ON a.编号 = e.门店编码
    ORDER BY a.事业部, a.开发区, 商品, 销售金额 DESC;

    /*==============================================================================
        第十一部分: 门店经营天数分析
    ==============================================================================*/
    
    -- 分析门店经营情况
    DECLARE @sdate VARCHAR(20);
    SET @sdate = '2024-01-01';

    -- 统计门店经营天数和销售额
    SELECT companycode,
           code AS storecode,
           COUNT(DISTINCT rq) AS 经营天数,
           SUM(noxse) AS 累计销售额,
           ROUND(SUM(noxse) / COUNT(DISTINCT rq), 2) AS 日均销售额
    INTO #TS
    FROM odsdbfq_result.dbo.m_stsale WITH (NOLOCK)
    WHERE rq >= @sdate 
      AND rq <= CONVERT(VARCHAR(20), GETDATE()-1, 23) 
      AND companycode = 'hn' 
      AND noxse > 0
    GROUP BY companycode, code;

    -- 关联门店信息
    SELECT a.*,
           b.shoptype,
           syb AS 事业部,
           -- 计算经营活跃度
           CASE WHEN a.经营天数 >= DATEDIFF(DAY, @sdate, GETDATE()-1) * 0.8 THEN '高活跃'
                WHEN a.经营天数 >= DATEDIFF(DAY, @sdate, GETDATE()-1) * 0.5 THEN '中活跃'
                ELSE '低活跃' END AS 经营活跃度,
           -- 计算经营天数占比
           ROUND(a.经营天数 * 100.0 / DATEDIFF(DAY, @sdate, GETDATE()-1), 2) AS 经营天数占比
    INTO #ts2
    FROM #TS a
    LEFT JOIN odsdbfq_basic.dbo.store b WITH (NOLOCK) 
        ON a.storecode = b.code AND b.CompanyCode = 'hn' AND stat = '有效';

    -- 更新特殊事业部
    UPDATE #ts2
    SET 事业部 = '休闲食品部' 
    WHERE storecode IN (
        SELECT DISTINCT 编号 FROM odsdbfqbi.dbo.storeinf WITH (NOLOCK)
        WHERE 事业部 = '休闲食品部'
    );

    -- 输出门店经营分析结果
    SELECT 事业部,
           shoptype AS 店型,
           COUNT(*) AS 门店数,
           SUM(经营天数) AS 总经营天数,
           ROUND(AVG(经营天数), 1) AS 平均经营天数,
           SUM(累计销售额) AS 总销售额,
           ROUND(AVG(日均销售额), 2) AS 平均日销额,
           SUM(CASE WHEN 经营活跃度 = '高活跃' THEN 1 ELSE 0 END) AS 高活跃门店数,
           ROUND(SUM(CASE WHEN 经营活跃度 = '高活跃' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS 高活跃门店占比
    FROM #ts2
    WHERE 事业部 IS NOT NULL
    GROUP BY 事业部, shoptype
    ORDER BY 事业部, 店型;

    /*==============================================================================
        第十二部分: 清理临时表
    ==============================================================================*/
    
    -- 清理所有临时表释放内存
    DROP TABLE IF EXISTS #moutdrpt;
    DROP TABLE IF EXISTS #ddplist;
    DROP TABLE IF EXISTS #sale_data1;
    DROP TABLE IF EXISTS #sale_data11;
    DROP TABLE IF EXISTS #sales0705;
    DROP TABLE IF EXISTS #sale_data2;
    DROP TABLE IF EXISTS #stk;
    DROP TABLE IF EXISTS #stk2;
    DROP TABLE IF EXISTS #sale01;
    DROP TABLE IF EXISTS #stk01;
    DROP TABLE IF EXISTS #stores;
    DROP TABLE IF EXISTS #store2;
    DROP TABLE IF EXISTS #TS;
    DROP TABLE IF EXISTS #ts2;
    
    PRINT '循环日销表V2分析完成，所有临时表已清理';

END TRY
BEGIN CATCH
    -- 错误处理
    DECLARE @ErrorMessage NVARCHAR(4000);
    DECLARE @ErrorSeverity INT;
    DECLARE @ErrorState INT;

    SELECT 
        @ErrorMessage = ERROR_MESSAGE(),
        @ErrorSeverity = ERROR_SEVERITY(),
        @ErrorState = ERROR_STATE();

    PRINT '执行过程中发生错误:';
    PRINT '错误信息: ' + @ErrorMessage;
    PRINT '错误级别: ' + CAST(@ErrorSeverity AS VARCHAR(10));
    PRINT '错误状态: ' + CAST(@ErrorState AS VARCHAR(10));
    
    -- 清理临时表
    DROP TABLE IF EXISTS #moutdrpt;
    DROP TABLE IF EXISTS #ddplist;
    DROP TABLE IF EXISTS #sale_data1;
    DROP TABLE IF EXISTS #sale_data11;
    DROP TABLE IF EXISTS #sales0705;
    DROP TABLE IF EXISTS #sale_data2;
    DROP TABLE IF EXISTS #stk;
    DROP TABLE IF EXISTS #stk2;
    DROP TABLE IF EXISTS #sale01;
    DROP TABLE IF EXISTS #stk01;
    DROP TABLE IF EXISTS #stores;
    DROP TABLE IF EXISTS #store2;
    DROP TABLE IF EXISTS #TS;
    DROP TABLE IF EXISTS #ts2;
    
    RAISERROR (@ErrorMessage, @ErrorSeverity, @ErrorState);
END CATCH;

-- 重置会话选项
SET NOCOUNT OFF;
SET ANSI_WARNINGS ON;
