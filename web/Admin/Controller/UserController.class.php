<?php 
namespace Admin\Controller;
use Think\Controller;

class UserController extends BaseController
{
	public function get_user(){
		$model = D('Keyword_res');
		$info = $model->search();
		//dump($info);die;
		$this->assign($info);
		$this->display();
	}

}

 ?>
