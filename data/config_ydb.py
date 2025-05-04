from data import cfg
from boto3 import resource


ydb_doc_api_client = resource('dynamodb',
                              endpoint_url=cfg.USER_STORAGE_URL,
                              region_name='us-east-1',
                              aws_access_key_id=cfg.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=cfg.AWS_SECRET_ACCESS_KEY)
table_message = ydb_doc_api_client.Table(cfg.base_message)
table_welcome = ydb_doc_api_client.Table(cfg.base_last_welcome)
table_temp = ydb_doc_api_client.Table(cfg.bl_temp)
table_bl = ydb_doc_api_client.Table(cfg.base_black_list)
table_banned_user = ydb_doc_api_client.Table(cfg.banned_user)
table_admin_temp = ydb_doc_api_client.Table(cfg.admin_temp)