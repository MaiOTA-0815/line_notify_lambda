# 📬 LINE通知Bot - 毎月の祈りを自動でお届けするBot  
**LINE Notification Bot - Monthly Prayers Delivered Automatically**

このプロジェクトは、**AWS Lambda** と **LINE Messaging API** を活用し、  
毎月 **1日と15日の朝9時** に、LINEグループや個人へ**自動通知**を送信するBotです。

> 忘れたくない、大切な想いを。そっと、やさしく届けます。

This project is a LINE bot built using **AWS Lambda** and the **LINE Messaging API**.  
It sends automatic notifications at **9:00 AM on the 1st and 15th of each month**,  
gently delivering important messages to loved ones.

---

## 🛠 技術構成 | Tech Stack

- Python 3.x  
- AWS Lambda（サーバーレス実行）  
- Amazon EventBridge（定期実行スケジューラー）  
- Amazon S3（デプロイ用ストレージ）  
- LINE Messaging API（通知配信）

---

## 💌 主な機能 | Key Features

- ⏰ **定時通知**：1日と15日の朝9時にメッセージを自動送信  
- 🔍 **グループID自動取得**：`join`イベント検知により自動でID取得  
- 🔐 **署名検証**：`X-Line-Signature` の検証でセキュリティ強化  
- 🔄 **通知モード切替**：スケジュール通知と手動テスト通知を切り替え可能  

---

## 🤝 ChatGPTと共に開発 | Built with ChatGPT's Support

このBotは、**ChatGPT**と共に開発されました。  
設計・実装・トラブル対応・文章作成まで、  
AIと人が**対話しながら**丁寧に仕上げたプロジェクトです。

> Each step was crafted through collaboration between human and AI —  
> a heartfelt journey built on gentle dialogue and shared curiosity.

---

## 🔐 利用ライセンス | License

このプロジェクトは  
[GNU General Public License v2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html) に準拠しています。  

✅ 利用・改変・再配布について | Usage & Permissions
このプロジェクトは、小さな宗教コミュニティ向けに開発されたものです。
現在のところ、無断での利用・改変・再配布はご遠慮ください。

もしこのBotを使用したい・参考にしたいとお考えの方がいらっしゃいましたら、
開発者までご連絡いただけると幸いです。

📩 開発者メールアドレス
maiohta3939★gmail.com（★を@に変えてください）

This project was developed for a small private religious community,
and at this time, unauthorized use, modification, or redistribution is not permitted.

If you are interested in using or referencing this bot,
please kindly contact the author beforehand.

📩 Email address
maiohta3939@gmail.com (replace "★" with "@")
- ⚠️ **ライセンス表示の保持** をお願いします  

---

## 🌱 作者より | From the Author

> 「忘れたくないことを、大切にしたい人に、そっと届けたい」

そんな想いからこのBotは生まれました。  
日々の中で、小さなやさしさや安心を届けられたら嬉しいです。

This bot was created out of a personal wish —  
to quietly deliver reminders and prayers to those I care about.  
I hope it brings gentle comfort into someone's daily life.

---
## 📝 更新履歴 | Changelog

- **2025-08-16**
  - 🔐 **環境変数対応 | Environment Variables Support**  
    - `CHANNEL_ACCESS_TOKEN`, `GROUP_ID`, `TEST_MODE` を Lambda 環境変数で管理するよう変更  
    - 秘密情報をコードに直書きせず、セキュリティと柔軟性が向上  
    - Moved sensitive values (`CHANNEL_ACCESS_TOKEN`, `GROUP_ID`, `TEST_MODE`) to Lambda environment variables  
    - Improved security and flexibility by removing hardcoded secrets
  - 🧪 **テストモード追加 | Test Mode**  
    - `TEST_MODE=true` を設定すると日付に関係なく通知を送信可能（デバッグ用）  
    - Added `TEST_MODE=true` option to send messages regardless of date (for debugging)  
  - ⚙️ **デプロイ手順整理 | Deployment Improvements**  
    - `function.zip` を `.gitignore` に追加し、不要な成果物をGitHubに含めないよう修正  
    - Refined deployment process by ignoring `function.zip` build artifact in GitHub  
    - `lambda_function.py` のロジック整理、ログ出力を改善  
    - Simplified `lambda_function.py` logic and improved logging  

- **2025-06-15**
  - 🎉 **初回リリース | Initial Release**  
    - AWS Lambda + EventBridge + LINE Messaging API を活用して、  
      毎月 **1日と15日の朝9時** にLINEグループへ自動通知を送信するBotを実装  
    - Implemented a bot using AWS Lambda + EventBridge + LINE Messaging API  
      to automatically send notifications to a LINE group at **9:00 AM on the 1st and 15th of each month**

---
## ⚠️ 注意事項 | Notes

このリポジトリ内の `lambda_function.py` では、  
**LINEのチャンネルトークン・チャネルシークレット・グループIDはダミー値**です。

本番環境での利用時は、[LINE Developers](https://developers.line.biz/)から発行された  
**正しい認証情報に置き換えてください。**

---

## 📎 GitHub Pages もしくは デモ（任意）

---

## 📣 フィードバック歓迎！

改善点・ご意見・応援など、IssueやPull Requestでお知らせいただけるととても嬉しいです🌸  
あなたの祈りのかたちにも、このBotが寄り添えますように。

