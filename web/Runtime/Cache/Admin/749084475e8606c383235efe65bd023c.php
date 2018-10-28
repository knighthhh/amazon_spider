<?php if (!defined('THINK_PATH')) exit();?><!DOCTYPE html>
<html lang="zh-cn">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<meta name="renderer" content="webkit">
<title></title>
<link rel="stylesheet" href="<?php echo (ADMIN_CSS_URL); ?>pintuer.css">
<link rel="stylesheet" href="<?php echo (ADMIN_CSS_URL); ?>admin.css">
<link rel="stylesheet" href="<?php echo (ADMIN_CSS_URL); ?>jquery-ui.min.css">
<link rel="stylesheet" href="<?php echo (ADMIN_LAYUI_URL); ?>css/layui.css">
<link rel="stylesheet" href="<?php echo (ADMIN_CSS_URL); ?>font-awesome.min.css">
<script src="<?php echo (ADMIN_JS_URL); ?>jquery.js"></script>
<script src="<?php echo (ADMIN_JS_URL); ?>jquery-ui.min.js"></script>
<script src="<?php echo (ADMIN_JS_URL); ?>pintuer.js"></script>
<style type="text/css">
	.dialogtable{border-collapse: collapse; width: 100%;padding-top: 12px;}
	.dialogtable th{background-color: #E8E8E8;}
	.dialogtable th,
	.dialogtable td{border: solid 1px #ccc; padding: 8px;valign:middle;}
	.button.border-green{ color:#22CC77;}
	.pagelist span.current{background: #22CC77}
	.level li{float:left;}
	.bread{}
</style>
</head>
<body>
<form method="post" action="/mountings/web/index.php/Admin/User/get_user" id="listform">
  <div class="panel admin-panel">
    <div class="padding border-bottom">
    </div>
    <table class="table table-hover text-center">
      <tr>
        <th width="25%" style="">ID</th>
        <th width="25%">name</th>
        <th width="25%" style="">password</th>
        <th width="25%"></th>
      </tr>
      <?php if(empty($data)): ?>
      		<tr>
      			<td></td>
      			<td></td>
      			<td></td>
      			<td>
      				<div style="padding:20px"><i class="layui-icon" style="font-size: 30px; color: #22CC77;">&#xe650;</i>空空如也~</div>
      			</td>
      		</tr>
      <?php endif; ?>
    <?php foreach ($data as $k => $v): ?>
        <tr>
          <td><?php echo $v['user_id']; ?></td>
          <td><?php echo $v['user_name']; ?></td>
          <td><?php echo $v['user_password']; ?></td>
          
        </tr>
        
    <?php endforeach; ?>
      <tr>
      	<td colspan="8">
      	<div class="pagelist">
      		<?php echo ($page); ?>
      		</div>
      	</td>
      </tr>
    </table>
</form>
<script src="<?php echo (ADMIN_LAYUI_URL); ?>lay/dest/layui.all.js"></script>
<script type="text/javascript">


</script>
</body>
</html>