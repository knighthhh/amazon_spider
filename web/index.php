<?php
//模式由生产模式变为开发模式
define("APP_DEBUG", True);


//define("SITE_URL", "http://139.199.166.127");
define("SITE_URL", "http://127.0.0.1");

//定义前台界面CSS,image,js路径
define("HOME_CSS_URL", "/amazon_spider/web/Public/Home/css");
define("HOME_IMAGES_URL", SITE_URL . "/amazon_spider/web/Public/Home/images");
define("HOME_JS_URL", SITE_URL . "/amazon_spider/web/Public/Home/js");
define("HOME_PUBLIC", SITE_URL . "/amazon_spider/web/Home/Public");

//定义后台界面CSS,image,js路径
define("ADMIN_CSS_URL", SITE_URL . "/amazon_spider/web/Public/Admin/css/");
define("ADMIN_IMAGES_URL", SITE_URL . "/amazon_spider/web/Public/Admin/images/");
define("ADMIN_JS_URL", SITE_URL . "/amazon_spider/web/Public/Admin/js/");

define("NCBI_URL", "https://www.ncbi.nlm.nih.gov/pubmed/");

//layui文件路径
#define("ADMIN_LAYUI_URL", SITE_URL . "/health/management/Application/Public/layui/");

require './ThinkPHP/ThinkPHP.php';
