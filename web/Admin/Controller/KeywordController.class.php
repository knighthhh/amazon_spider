<?php 
namespace Admin\Controller;
use Think\Controller;

class KeywordController extends BaseController
{
	public function get_res(){
		$model = D('Keyword_res');
		$info = $model->search();
		//dump($info);die;
		$this->assign($info);
		$this->display();
	}

    public function analyze(){
		$model = D('Keyword_res');
		$info = $model->search();
		$this->assign($info);
		//$this->display();
	}

	public function sort_res(){
		$model = D('Keyword_res');
		$info = $model->sort_res();
		$this->assign($info);
		$this->display(get_res);
	}

    public function export_excel(){
        import("Org.Util.PHPExcel");
        import("Org.Util.PHPExcel.IOFactory", '', '.php');
        //创建PHPExcel对象，注意，不能少了\
        $objPHPExcel = new \PHPExcel();
        //$objPHPExcel->getProperties()->setCreator("文件作者信息...")
          //          ->setLastModifiedBy("文件最后修改作者")
            //        ->setTitle("文件标题")
              //      ->setSubject("这是啥啊")
                //    ->setDescription("文件描述")
                  //  ->setKeywords("文件关键词 貌似是用空格隔开")
                    //->setCategory("Test result file");

        $objPHPExcel->getProperties()->setTitle("文件标题");

        // 添加第一栏数据
        $objPHPExcel->setActiveSheetIndex(0)
                    ->setCellValue('A1', '产品id')
                    ->setCellValue('B1', '标题')
                    ->setCellValue('C1', 'url')
                    ->setCellValue('D1', '价格(美元)')
                    ->setCellValue('E1', '颜色')
                    ->setCellValue('F1', '尺寸')
                    ->setCellValue('G1', '评论数')
                    ->setCellValue('H1', '评论评分')
                    ->setCellValue('I1', '是否有跟卖')
                    ->setCellValue('J1', '跟卖数量')
                    ->setCellValue('K1', '编号')
                    ->setCellValue('L1', '排名1')
                    ->setCellValue('M1', '分类1')
                    ->setCellValue('N1', '排名2')
                    ->setCellValue('O1', '分类2')
                    ->setCellValue('P1', '爬取时间戳')
                    ->setCellValue('Q1', '爬取时间');
        //二维数组 从数据库拿出来
        $excelData = D('Keyword_res')->select();
        for ($i=2;$i<count($excelData)+2;$i++){
            $objPHPExcel->setActiveSheetIndex(0)
                        ->setCellValue('A'.$i, $excelData[$i-2]['product_id'])
                        ->setCellValue('B'.$i, $excelData[$i-2]['title'])
                        ->setCellValue('C'.$i, $excelData[$i-2]['url'])
                        ->setCellValue('D'.$i, $excelData[$i-2]['price'])
                        ->setCellValue('E'.$i, $excelData[$i-2]['color'])
                        ->setCellValue('F'.$i, $excelData[$i-2]['size'])
                        ->setCellValue('G'.$i, $excelData[$i-2]['commentcount'])
                        ->setCellValue('H'.$i, $excelData[$i-2]['commentrating'])
                        ->setCellValue('I'.$i, $excelData[$i-2]['have_follow_sale'])
                        ->setCellValue('J'.$i, $excelData[$i-2]['follow_sale_num'])
                        ->setCellValue('K'.$i, $excelData[$i-2]['asin'])
                        ->setCellValue('L'.$i, $excelData[$i-2]['rank1'])
                        ->setCellValue('M'.$i, $excelData[$i-2]['category1'])
                        ->setCellValue('N'.$i, $excelData[$i-2]['rank2'])
                        ->setCellValue('O'.$i, $excelData[$i-2]['category2'])
                        ->setCellValue('P'.$i, $excelData[$i-2]['crawled_timestamp'])
                        ->setCellValue('Q'.$i, $excelData[$i-2]['crawled_time']);
        }

        // 设置下边的文章标题 我也不知道叫啥
        $objPHPExcel->getActiveSheet()->setTitle('结果');
        // 设置打开文件浏览的页面（0为第一页）
        $objPHPExcel->setActiveSheetIndex(0);
        // 保存为Excel 2007 文件
        $callStartTime = microtime(true);
        $objWriter = \PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel5');
        $objWriter->save(str_replace('.php', '.xls', 'amazon'));
        $callEndTime = microtime(true);
        $callTime = $callEndTime - $callStartTime;
        // Redirect output to a client’s web browser (Excel2007)
        header('Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
        header('Content-Disposition: attachment;filename="amazon_results.xlsx"');
        header('Cache-Control: max-age=0');
        // If you're serving to IE 9, then the following may be needed
        header('Cache-Control: max-age=1');
        // If you're serving to IE over SSL, then the following may be needed
        header ('Expires: Mon, 26 Jul 1997 05:00:00 GMT'); // Date in the past
        header ('Last-Modified: '.gmdate('D, d M Y H:i:s').' GMT'); // always modified
        header ('Cache-Control: cache, must-revalidate'); // HTTP/1.1
        header ('Pragma: public'); // HTTP/1.0
        $objWriter = \PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel2007');
        $objWriter->save('php://output');

    }
}

 ?>
