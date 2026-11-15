# 互動式閱讀測驗 Skill（reading-quiz）

一個給 [Claude Code](https://claude.com/claude-code) 用的 skill：貼上一篇文章，說「做閱讀測驗」，Claude 就會出題，並產生一個**單一 HTML 檔**的互動式閱讀測驗網頁。

設計對象是需要報讀支持的國中學習障礙、閱讀理解較弱的學生，一般班級也可以用。

👉 **線上試玩**：[demo/index.html](demo/index.html)（下載後用瀏覽器打開即可；開啟 GitHub Pages 後也可直接線上操作）

## 網頁有什麼

**閱讀**
- 文章逐段出現，每段倒數幾秒才能看下一段，避免學生跳讀直接猜答案
- 點一下句子就朗讀（加底線），連點兩下劃重點
- 段落旁的喇叭朗讀整段
- 設定裡可調報讀語速、字體大小、行距

**作答**
- 讀完後畫面換到題目；右上角「顯示文章」可回看原文（電腦左右並排，手機全螢幕）
- 題目、選項、詳解、提示都可以報讀
- **練習模式**：答錯不直接公布答案，先給分層提示
  1. 「回到第 N 段再讀一次」，該段加框
  2. 把證據句標出來
  3. 再錯才公布答案和詳解
- **測驗模式**：答完立即公布

**紀錄**
- 結果頁分開計算「第一次就答對」和「用提示後答對」
- 可下載兩個 CSV（Excel 開啟不會亂碼）：
  - 作答摘要：每題作答順序、次數、使用提示、回看文章次數、秒數
  - 操作紀錄：每個動作的時間，例如朗讀哪一句、劃了哪裡、何時打開文章
- 不需要伺服器或帳號，資料只存在使用者的瀏覽器

## 安裝

把 `reading-quiz` 資料夾複製到 Claude Code 的 skills 資料夾：

```bash
git clone https://github.com/chuoneone/reading-quiz-skill.git
```

- Windows：複製到 `C:\Users\<你的帳號>\.claude\skills\reading-quiz`
- macOS／Linux：複製到 `~/.claude/skills/reading-quiz`

需要 Python 3（產生網頁用，不需另外安裝套件）。

## 使用

在 Claude Code 裡貼上文章，然後說：

> 幫我把這篇做成閱讀測驗，放桌面

Claude 會：
1. 把文章分段、出 4 題（由淺到深：擷取 → 推論 → 主旨）
2. 寫成資料檔（JSON），每題附上證據段落和證據句
3. 執行 `scripts/build_page.py` 套進固定範本，產生 HTML

也可以自己寫 JSON，直接執行：

```bash
python reading-quiz/scripts/build_page.py reading-quiz/examples/會說話的路.json 輸出.html
```

資料檔格式見 [`reading-quiz/SKILL.md`](reading-quiz/SKILL.md) 的「資料檔規格」，範例見 [`reading-quiz/examples/會說話的路.json`](reading-quiz/examples/會說話的路.json)。

## 配色

`theme` 有兩種：`minimal`（簡約：墨藍、米白、橘色重點，預設）和 `classic`（藍綠色）。

## 授權

© 2025 特教米克師。本作品採用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh_TW) 授權：

- 歡迎非商業用途使用、轉載、改編
- 請保留「特教米克師」署名並附上本專案連結
- 改編後的作品請用相同授權分享

產生的網頁頁尾會自動帶上這段授權說明，請勿移除。
