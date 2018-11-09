<?php 
namespace Admin\Controller;
use Think\Controller;

class BestsellerController extends BaseController
{
	public function get_res(){
		$model = D('Keyword_res');
		$info = $model->search();
		//dump($info);die;
		$this->assign($info);
		$this->display();
	}


}

?>
