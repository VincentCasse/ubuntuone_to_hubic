<?php
	if (isset($_REQUEST['error_description'])) {
		$error = htmlEntities($_GET['error_description'], ENT_QUOTES);
	}  else {
		$code = base64_decode($_GET['code'], true);
		if (!$code) {
			$code = 'There is no code !';
		} else {
			$code = htmlEntities($_GET['code'], ENT_QUOTES);
		}
	}
?>
<html>
	<head>
		<title>Get your code</title>
		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">

		<!-- Optional theme -->
		<link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css">

		<!-- Latest compiled and minified JavaScript -->
		<script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>

		<link href='https://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>

		<style type="text/css">
			body {
				background-color: #0C6898;
				font-family: 'Open Sans', sans-serif;
				max-width: 1080px;
				margin: auto;
			}
			body article {
				height: 400px;
				padding: 50px 0;
				color: white;
			}
			body footer {
				color: white;
				
				text-align: right;
				font-size: 0.8em;
			}
			.panel-body {
				background-color: #F5F3EC;
				color: black;
			}
		</style>
	</head>

	<body>
		<header class="row">
			<div class="col-xs-10 col-xs-offset-1">
				<img src="https://hubic.com/home/static/images/logo.png" alt="hubiC" />
			</div>
		</header>

		<article class="row">
			<div class="col-xs-10 col-xs-offset-1">

				<?php if (isset($error)): ?>

					<h2>Error : </h2>

					<div class="panel panel-danger">
						<div class="panel-heading">
							<?php echo $error; ?>
						</div>
					</div>

				<?php else: ?>

					<h2>Your code is :</h2>

					<div class="panel panel-default">
						<div class="panel-body">
							<?php echo $code; ?>
						</div>
					</div>

				<?php endif; ?>
				
			</div>
		</article>

		<footer class="row">
			<div class="col-xs-10 col-xs-offset-1">
				Unofficial webpage <br />
				Be safe with this code, developers could be dangerous with it !
			</div>
		</footer>
	</body>
</html>