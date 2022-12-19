import boto3

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):

    # 起動インスタンスのキー
    ec2_detail_key = 'resource-id'
    
    # 起動インスタンスのID
    ec2_detail_value = event['detail']['instance-id']
    
    # アカウント情報
    account = event['account']
    
    # 状態
    state = event['detail']['state']
    
    # 起動インスタンスを元にタグ取得
    describe_tags_list = ec2.describe_tags(
        Filters=[
            {
                'Name': ec2_detail_key,
                'Values': [ec2_detail_value],
            },
        ]
    )
    
    #EC2のNameタグ
    ec2_tag_detail = get_tag_detail(describe_tags_list)

    #snsトピックのARN
    topic_arn = ''
    
    #件名
    subject = '【周知】『' + ec2_tag_detail + '』EC2インスタンス起動'
    
    #本文
    message = '対象サーバー： 「' + ec2_tag_detail + '」が正常に起動中です。'\
    + '\n' + '\n' + 'AccountID： 「' + account + '」'  + '\n'\
    + '\n' + '状態： 「' + state + '」' + '\n'\
    + '\n' + '※使わない時は極力停止してください。その際、連絡は必ずしてください。' + '\n'\
    +'※再起動する際は、別途でメールを送信してください。'
    
    #sns情報
    sns_info = get_sns_detail(topic_arn, subject, message)
    
    #サブスクリプションへ
    sns.publish(**sns_info)

'''
#タグの詳細取得
@para dict describe_tags_list: EC2のタグ全て

@return Nameのタグ情報
'''
def get_tag_detail(describe_tags_list):
    
    #初期値:str
    get_ec2_tag = None
    
    # EC2タグの詳細の初期値:dict 
    get_ec2_tag_detail = {}
    
    # KeyがNameのValueを取得
    get_ec2_tag_detail = [d.get('Value') for d in describe_tags_list['Tags'] if d.get('Key') == 'Name']
    
    # NameタグのValueがあるのかの判定
    if not get_ec2_tag_detail[0]:
        get_ec2_tag_detail[0] = 'Tag名がないEC2'
        get_ec2_tag = get_ec2_tag_detail[0]
    else:
        # dictから文字型
        get_ec2_tag = get_ec2_tag_detail[0]

    return get_ec2_tag

'''
#メール情報を詰める

@param str topic_arn: topicのARN
@param str subject: 件名
@param str message: 本文

@return get_sns_info: メール情報
'''
def get_sns_detail(topic_arn, subject, message):
    
    # SNS
    get_sns_info = {
        'TopicArn': topic_arn,
        'Subject': subject,
        'Message': message
    }
    
    return get_sns_info