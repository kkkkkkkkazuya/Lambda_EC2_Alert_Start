# Lambda_EC2_Alert_Start
EC2からEventBridge、Lambda、SNSへのアーキテクチャ構成。

本文や件名を変更するためにLambdaを入れている。

EC2起動時に、EC2情報をEventBridgeでLambdaに送り、そのEC2情報を元にLambdaで、
EC2のタグNameを取り、本文をカスタマイズしてSNSでサブスクライブする構成。