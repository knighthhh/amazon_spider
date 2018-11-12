<?php 
namespace Admin\Controller;
use Think\Controller;

class BestsellerController extends BaseController
{
	public function get_bestseller(){

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

	public function get_item(){
		$model = M('bestseller');
	    $data['typeid'] = I('post.query_id');
        $res = $model->where($data) -> select();
    	echo json_encode($res);
	}

}

?>
