<?php 
namespace Admin\Controller;
use Think\Controller;

class BestsellerController extends BaseController
{
	public function get_bestseller(){
		$model = D('Keyword_res');
		$info = $model->search();
		//dump($info);die;
		$this->assign($info);
		$this->display();
	}


    public function get_levelone(){
		$model = M('onedepa');
        $res = $model -> select();
    	echo json_encode($res);
	}

	public function get_leveltwo(){
		$model = M('twodepa');
	    $data['pid'] = I('post.pid');
        $res = $model->where($data) -> select();
    	echo json_encode($res);
	}

    public function get_levelthree(){
		$model = M('threedepa');
	    $data['pid'] = I('post.pid');
        $res = $model->where($data) -> select();
    	echo json_encode($res);
	}
}

?>
