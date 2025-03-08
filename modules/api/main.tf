module "aws_s3_bucket" {
  source = "../s3_deploy"
  tags = {
    Terraform   = "true"
    Environment = "dev"
  }
}

# API Gateway
resource "aws_api_gateway_rest_api" "public_api" {
  name        = "Public API"
  description = "This is the Public API"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.public_api.id
  parent_id   = aws_api_gateway_rest_api.public_api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.public_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "public_api" {
  rest_api_id = aws_api_gateway_rest_api.public_api.id
  resource_id = aws_api_gateway_method.proxy.resource_id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.public_api.invoke_arn
}

resource "aws_api_gateway_method" "proxy_root" {
  rest_api_id   = aws_api_gateway_rest_api.public_api.id
  resource_id   = aws_api_gateway_rest_api.public_api.root_resource_id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "public_api_root" {
  rest_api_id = aws_api_gateway_rest_api.public_api.id
  resource_id = aws_api_gateway_method.proxy_root.resource_id
  http_method = aws_api_gateway_method.proxy_root.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.public_api.invoke_arn
}

resource "aws_api_gateway_deployment" "public_api" {
  depends_on = [
    aws_api_gateway_integration.public_api,
    aws_api_gateway_integration.public_api_root,
  ]

  rest_api_id = aws_api_gateway_rest_api.public_api.id
}

resource "aws_api_gateway_stage" "public_api" {
  deployment_id = aws_api_gateway_deployment.public_api.id
  rest_api_id   = aws_api_gateway_rest_api.public_api.id
  stage_name    = "dev"
}


# Lambdas
resource "aws_s3_object" "file_upload" {
  bucket = module.aws_s3_bucket.name
  key    = "api_source.zip"
  source = "${data.archive_file.public_api_source.output_path}"
  etag = filemd5("${data.archive_file.public_api_source.output_path}")
}

resource "aws_iam_role" "iam_for_public_api" {
  name               = "iam_for_public_api"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_lambda_function" "public_api" {
  s3_bucket         = module.aws_s3_bucket.name
  s3_key            = aws_s3_object.file_upload.key
  
  function_name = var.lambda_function_name
  role          = aws_iam_role.iam_for_public_api.arn
  handler       = "public_api.handler"

  source_code_hash = aws_s3_object.file_upload.etag

  runtime = "nodejs20.x"
  publish = true

  logging_config {
    log_format = "Text"
  }

  depends_on = [
    aws_iam_role_policy_attachment.public_api_logging,
    aws_cloudwatch_log_group.public_api,
  ]
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.public_api.function_name}"
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.public_api.execution_arn}/*/*"
}

# Cloudwatch Logs

resource "aws_cloudwatch_log_group" "public_api" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 365
}

resource "aws_iam_policy" "public_api_logging" {
  name        = "public_api_logs"
  path        = "/"
  description = "IAM policy for logging from a lambda"
  policy      = data.aws_iam_policy_document.lambda_logging.json
}

resource "aws_iam_role_policy_attachment" "public_api_logging" {
  role       = aws_iam_role.iam_for_public_api.name
  policy_arn = aws_iam_policy.public_api_logging.arn
}
