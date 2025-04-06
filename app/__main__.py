from modules.config import model,get_db_url
from modules.agent import PresentationAgent
from modules.models import Persona,InterviewResult,InterviewContent,PersonaList
import argparse
from langgraph.checkpoint.postgres import PostgresSaver
def main():
    with PostgresSaver.from_conn_string(get_db_url()) as checkpointer:
        parser = argparse.ArgumentParser()
        parser.add_argument("--id",type=str,default="")
        parser.add_argument("--skip",type=str,default="")
        args = parser.parse_args()
        # persona_generator = PersonaGenerator(model, "ITベンチャー企業です")
        # result = persona_generator.run("AWSについての勉強会を開きますが、どのようなコンテンツが良いでしょうか")
        # print(result)
        # interview_conductor = InterviewConductor(model)
        # result = interview_conductor.run(
        #     personas=[
        #         Persona(name="佐藤健太",background="28歳男性、開発部門のエンジニア。大学で情報工学を専攻し、現在はフルスタック開発に従事。AWSの基本的な知識はあるが、実務経験は浅い。新しい技術を学ぶことに意欲的で、特にクラウドサービスの活用に興味を持っている。"),
        #         Persona(name="山田美咲",background="35歳女性、マーケティング部門のマネージャー。IT業界での経験は10年以上で、デジタルマーケティングに特化している。AWSについては知識が乏しいが、データ分析や顧客管理におけるクラウドの利点を理解したいと考えている。"),
        #         Persona(name="鈴木一郎",background="45歳男性、システム管理部門のリーダー。長年のITインフラ管理の経験があり、AWSの導入を検討している。技術的な専門知識は豊富だが、最新のクラウド技術に関してはキャッチアップが必要と感じている。")
        #     ],
        #     user_request="AWSについての勉強会を開きますが、どのようなコンテンツが良いでしょうか")
        # information_evaluator = InformationEvaluator(model)
        personas:PersonaList=PersonaList(personas=[
            Persona(name="佐藤健太",background="28歳男性、開発部門のエンジニア。大学で情報工学を専攻し、現在はフルスタック開発に従事。AWSの基本的な知識はあるが、実務経験は浅い。新しい技術を学ぶことに意欲的で、特にクラウドサービスの活用に興味を持っている。"),
            Persona(name="山田美咲",background="35歳女性、マーケティング部門のマネージャー。IT業界での経験は10年以上で、デジタルマーケティングに特化している。AWSについては知識が乏しいが、データ分析や顧客管理におけるクラウドの利点を理解したいと考えている。"),
            Persona(name="鈴木一郎",background="45歳男性、システム管理部門のリーダー。長年のITインフラ管理の経験があり、AWSの導入を検討している。技術的な専門知識は豊富だが、最新のクラウド技術に関してはキャッチアップが必要と感じている。")
        ])
        interview_result = InterviewResult(interview_contents=(
            InterviewContent(
                persona=Persona(
                    name='佐藤健太',
                    background='28歳男性、開発部門のエンジニア。大学で情報工学を専攻し、現在はフルスタック開発に従事。AWSの基本的な知識はあるが、実務経験は浅い。新しい技術を学ぶことに意欲的で、特にクラウドサービスの活用に興味を持っている。'
                ),
                question='AWSの勉強会で特に興味を持っている分野や、実務で直面している具体的な課題は何ですか？それに基づいて、どのようなコンテンツが最も役立つと感じますか？',
                answer='AWSの勉強会で特に興味を持っている分野は、クラウドアーキテクチャの設計や、サーバーレスアーキテクチャの活用です。特に、AWS LambdaやAPI Gatewayを使ったアプリケーションの構築に興味があります。実務では、スケーラビリティやコスト管理に関する課題に直面しており、特にトラフィックの変動に応じたリソースの最適化が難しいと感じています。\n\nそのため、以下のようなコンテンツが最も役立つと感じます：\n\n1. **実践的なハンズオンセッション**: AWSの各サービスを使った具体的なプロジェクトを通じて、実際のアーキテクチャを設計・構築する経験が得られると良いです。\n\n2. **ケーススタディ**: 成功事例や失敗事例を通じて、どのようにスケーラビリティやコスト管理を実現したのかを学ぶことができると、実務に役立つ知識が得られます。\n\n3. **ベストプラクティスの共有**: AWSの各サービスを効果的に活用するためのベストプラクティスや、よくある落とし穴についての情報があると、実務での判断に役立ちます。\n\n4. **Q&Aセッション**: 実務で直面している具体的な課題について、専門家に直接質問できる機会があると、より具体的な解決策を得られると思います。\n\nこれらのコンテンツを通じて、AWSの知識を深め、実務での課題解決に繋げていきたいと考えています。'
            ),
            InterviewContent(
                persona=Persona(
                    name='山田美咲',
                    background='35歳女性、マーケティング部門のマネージャー。IT業界での経験は10年以上で、デジタルマーケティングに特化している。AWSについては知識が乏しいが、データ分析や顧客管理におけるクラウドの利点を理解したいと考えている。'
                ),
                question='AWSの勉強会で、データ分析や顧客管理におけるクラウドの利点を具体的に理解するために、どのような実践的なケーススタディや成功事例を取り入れると、山田美咲さんにとって最も有益だと考えますか？',
                answer='山田美咲です。AWSの勉強会でデータ分析や顧客管理におけるクラウドの利点を具体的に理解するためには、以下のような実践的なケーススタディや成功事例を取り入れると有益だと思います。\n\n1. **顧客データの統合と分析**:\n   - ある企業がAWSを利用して、複数のデータソース（CRM、ウェブサイト、SNSなど）から顧客データを統合し、Amazon Redshiftを使ってデータ分析を行った事例。これにより、顧客の行動パターンを把握し、ターゲットマーケティングを実施した結果、売上が向上したという具体的な数字を示すと理解が深まります。\n\n2. **リアルタイムデータ分析**:\n   - AWSのKinesisを利用して、リアルタイムで顧客の行動データを分析し、即座にマーケティング施策を調整した企業の事例。例えば、特定のキャンペーンが効果的であることをリアルタイムで把握し、広告予算を最適化した結果、ROIが向上したという具体的な成果を紹介すると良いでしょう。\n\n3. **機械学習を活用した顧客予測**:\n   - Amazon SageMakerを使用して、顧客の購買予測モデルを構築した企業の事例。過去の購買データを基に、どの顧客が次に何を購入するかを予測し、パーソナライズされたオファーを提供した結果、顧客のリピート率が向上したという成功事例を取り上げると、機械学習の実用性が理解しやすくなります。\n\n4. **コスト削減とスケーラビリティ**:\n   - AWSのクラウドサービスを利用することで、オンプレミスのインフラを持たずに済み、必要に応じてリソースをスケールアップ・ダウンできる事例。特に、季節的な需要の変動に対応するために、AWSを活用してコストを削減した企業の成功事例を紹介すると、クラウドの利点が具体的にイメージしやすくなります。\n\nこれらのケーススタディを通じて、AWSの具体的な活用方法やその効果を理解することで、デジタルマーケティングにおけるクラウドの利点を実感できると思います。'
            ),
            InterviewContent(
                persona=Persona(
                    name='鈴木一郎',
                    background='45歳男性、システム管理部門のリーダー。長年のITインフラ管理の経験があり、AWSの導入を検討している。技術的な専門知識は豊富だが、最新のクラウド技術に関してはキャッチアップが必要と感じている。'
                ),
                question='鈴木一郎さんがAWSの導入を検討している中で、特にどのような業務課題やシステム要件を解決するためのAWSの機能やサービスに焦点を当てたコンテンツが最も役立つと考えていますか？',
                answer='鈴木一郎です。AWSの導入を検討する中で、特に以下の業務課題やシステム要件に焦点を当てたコンテンツが役立つと考えています。\n\n1. **コスト管理と最適化**: AWSの料金体系は複雑で、リソースの利用状況に応じたコスト管理が重要です。AWS Cost ExplorerやAWS Budgetsを活用したコスト最適化の方法についての具体的な事例やベストプラクティスが知りたいです。\n\n2. **スケーラビリティとパフォーマンス**: ビジネスの成長に伴い、システムのスケーラビリティが求められます。AWSのAuto ScalingやElastic Load Balancingを利用したスケーラブルなアーキテクチャの設計方法についての情報が役立ちます。\n\n3. **セキュリティとコンプライアンス**: クラウド環境でのデータセキュリティは非常に重要です。AWS Identity and Access Management (IAM)やAWS Shield、AWS WAFなどのセキュリティサービスを活用したセキュリティ対策の具体例や、コンプライアンスに関するガイドラインが必要です。\n\n4. **バックアップと災害復旧**: データのバックアップや災害復旧の計画は欠かせません。AWS BackupやAmazon S3のバージョニング機能を利用した効果的なバックアップ戦略についての情報が求められます。\n\n5. **マイグレーション戦略**: 既存のオンプレミスシステムからAWSへの移行をスムーズに行うためのマイグレーション戦略やツール（AWS Migration HubやAWS Application Migration Serviceなど）についての具体的な手順や成功事例が知りたいです。\n\nこれらの課題に対する具体的な解決策や事例を通じて、AWSの導入をよりスムーズに進められると考えています。'
            )
        ))
        # result = information_evaluator.run(
        #     interview_result=interview_result,
        #     user_request="AWSについての勉強会を開きますが、どのようなコンテンツが良いでしょうか"
        # )
        checkpointer.setup()
        presentation_agent = PresentationAgent(model,k=3,checkpointer=checkpointer)
        if(args.id):
            list = personas.personas
        else:
            if(args.skip):
                list = personas.personas
            else:
                list = []
        
        result = presentation_agent.run(user_request="AWSについての勉強会を開きますが、どのようなコンテンツが良いでしょうか",common_background="ITベンチャー企業に勤めています",thread_id=args.id,persona_list=list)
        print(result)
if __name__ == "__main__":
    main()
# source venv/bin/activate
# python app --id=5c67e314-5875-4c5c-9fba-a656b8cd12e4再度
# python app --skip=1 スキップ
# python app フルコース