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
		$this->display();
	}

	 public function export(){
		$model = D('Keyword_res');
		$info = $model->search();
		$this->assign($info);
		$this->display();
	}

	public function sort_res(){
		$model = D('Keyword_res');
		$info = $model->sort_res();
		$this->assign($info);
		$this->display(get_res);


	}

}

 ?>
