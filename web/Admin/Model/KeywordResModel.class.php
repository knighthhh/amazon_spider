<?php
namespace Admin\Model;
use Think\Model;

class KeywordResModel extends Model{
	public function search($perPage=10)
	{
		/* 分页 */
        $count = $this->count();
         /*搜索*/
        $where = array();
        $searchValue = I('post.searchValue');
        if($searchValue){
          $where['keywordtype'] = array('like',"%$searchValue%");
        }
        //实例化翻页类对象
        $pageObj = new \Think\Page($count, $perPage);
        //设置翻页样式
        $pageObj->setConfig('next', '下一页');
        $pageObj->setConfig('prev', '上一页');
        //生成翻页按钮（上一页，下一页）
        $pageButton = $pageObj->show();
        $data       = $this
            ->where($where)
            ->limit($pageObj->firstRow . "," . $pageObj->listRows)
            ->select();

        //处理跟卖
        foreach($data as $k=>$v){
             $product_id = $v['product_id'];
             $follow_where =  array();
             $images_where =  array();
             $follow_where['product_id'] = array('eq',$product_id);
             $images_where['product_id'] = array('eq',$product_id);
             $follow_sale = M(Follow_sale)
                    ->where($follow_where)
                    ->select();
             $images = M(Image)
                    ->where($images_where)
                    ->select();
             $data[$k]['follow_sale'] = $follow_sale;
             $data[$k]['images'] = $images;

        }

         //处理url词频统计
        foreach($data as $k=>$v){
            $url = $v['url'];
            preg_match('/https:\/\/www.amazon.com\/([^.]+)\/dp\//',$url, $matches);
            $match_res = $matches[1];
            $split_res = explode("-",$match_res);
            $res = array_count_values($split_res);
            $data[$k]['count_url'] = $res;
        }

        return array(
            'data' => $data, //用户信息
            'page' => $pageButton, //分页结果
        );
	}

	public function sort_res($perPage=10)
	{
	    $price = $_GET['price'];
	    $comment = $_GET['comment'];
	    $commentRating = $_GET['commentRating'];
	    $follow = $_GET['follow'];
	    $min = $_GET['min'];
	    $max = $_GET['max'];
	    $between_type = $_GET['between_type'];
	    $where = array();

	    $searchValue = I('post.searchValue');
	    print_r($searchValue);
        if($searchValue){
          $where['keywordtype'] = array('like',"%$searchValue%");
        }

	    if($between_type=='price'){
            $where['price'] = array('egt',$min);
            $where['price'] = array('elt',$max);
	    }else if($between_type=='comment'){
            $where['commentCount'] = array('egt',$min);
            $where['commentCount'] = array('elt',$max);
	    }else if($between_type=='commentRating'){
            $where['commentRating'] = array('egt',$min);
            $where['commentRating'] = array('elt',$max);
	    }else if($between_type=='follow'){
            $where['follow_sale_num'] = array('egt',$min);
            $where['follow_sale_num'] = array('elt',$max);
	    }



        $temparr = array();
        if($price == '1'){
            array_push($temparr,'price desc');
        }else if($price == '2'){
            array_push($temparr,'price asc');
        }

        if($comment == '1'){
            array_push($temparr,'commentCount desc');
        }else if($comment == '2'){
            array_push($temparr,'commentCount asc');
        }

        if($commentRating == '1'){
            array_push($temparr,'commentRating desc');
        }else if($commentRating == '2'){
            array_push($temparr,'commentRating asc');
        }

        if($follow == '1'){
            array_push($temparr,'follow_sale_num desc');
        }else if($follow == '2'){
            array_push($temparr,'follow_sale_num asc');
        }

        $orderstr = join(",",$temparr);

        $count = $this->count();

        //实例化翻页类对象
        $pageObj = new \Think\Page($count, $perPage);
        $pageObj->setConfig('next', '下一页');
        $pageObj->setConfig('prev', '上一页');
        $pageButton = $pageObj->show();

        $data       = $this
            ->order($orderstr)
            ->where($where)
            ->limit($pageObj->firstRow . "," . $pageObj->listRows)
            ->select();

        //处理跟卖
        foreach($data as $k=>$v){
             $product_id = $v['product_id'];
             $follow_where =  array();
             $images_where =  array();
             $follow_where['product_id'] = array('eq',$product_id);
             $images_where['product_id'] = array('eq',$product_id);
             $follow_sale = M(Follow_sale)
                    ->where($follow_where)
                    ->select();
             $images = M(Image)
                    ->where($images_where)
                    ->select();
             $data[$k]['follow_sale'] = $follow_sale;
             $data[$k]['images'] = $images;

        }

         //处理url词频统计
        foreach($data as $k=>$v){
            $url = $v['url'];
            preg_match('/https:\/\/www.amazon.com\/([^.]+)\/dp\//',$url, $matches);
            $match_res = $matches[1];
            $split_res = explode("-",$match_res);
            $res = array_count_values($split_res);
            $data[$k]['count_url'] = $res;
        }

        return array(
            'data' => $data, //用户信息
            'page' => $pageButton, //分页结果
        );
	}

	#分析
	public function analyze($perPage=10)
	{
        $count = $this->count();

        $where = array();
        //$searchValue = I('post.searchValue');
        //if($searchValue){
          //$where['keywordtype'] = array('like',"%$searchValue%");
        //}

        //实例化翻页类对象
        $pageObj = new \Think\Page($count, $perPage);
        //设置翻页样式
        $pageObj->setConfig('next', '下一页');
        $pageObj->setConfig('prev', '上一页');
        //生成翻页按钮（上一页，下一页）
        $pageButton = $pageObj->show();
        $data       = $this
            ->where($where)
            ->field('keywordtype,count(*) as num,sum(price)/count(*) as avgprice,sum(commentCount)/count(*) as avgcomment,sum(commentRating)/count(*) as avgrating,sum(follow_sale_num)/count(*) as avgfollow')
            ->group('keywordtype')
            ->limit($pageObj->firstRow . "," . $pageObj->listRows)
            ->select();

         //处理url词频统计
        //foreach($data as $k=>$v){
          //  $url = $v['url'];
            //preg_match('/https:\/\/www.amazon.com\/([^.]+)\/dp\//',$url, $matches);
            //$match_res = $matches[1];
            //$split_res = explode("-",$match_res);
            //$res = array_count_values($split_res);
            //$data[$k]['count_url'] = $res;
        //}

        return array(
            'data' => $data, //用户信息
            'page' => $pageButton, //分页结果
        );
	}


	protected function _before_insert(&$data,$option){

		
	}

	 protected function _before_update(&$data,$option)
    {
        
    }

    protected function _before_delete($option){
    	
    }
}


?>
