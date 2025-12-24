use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashMap;

// 预编译正则表达式
lazy_static! {
    static ref ANSI_REGEX: Regex = Regex::new(r#"\x1B\[[0-9;]*[mK]"#).unwrap();
    static ref CODE_BLOCK_REGEX: Regex = Regex::new(r#"```(\w+)?\n([\s\S]*?)```\n*"#).unwrap();
    static ref STRING_REGEX: Regex = Regex::new(r#"\"[^\"]*\"|'[^']*'"#).unwrap();
    static ref COMMENT_REGEX: Regex = Regex::new(r#"#.*$"#).unwrap();
    static ref KEYWORD_REGEX: Regex = Regex::new(r#"\b(if|elif|else|for|while|def|class|return|import|from|as|with|try|except|finally|raise|yield|async|await|break|continue|pass|del|global|nonlocal)\b"#).unwrap();
    static ref NUMBER_REGEX: Regex = Regex::new(r#"\b\d+(\.\d+)?\b"#).unwrap();
    static ref FUNCTION_REGEX: Regex = Regex::new(r#"\b([a-zA-Z_]\w*)\s*\("#).unwrap();
    static ref CLASS_REGEX: Regex = Regex::new(r#"\bclass\s+([a-zA-Z_]\w*)\b"#).unwrap();
}

// 主题定义
trait Theme {
    fn get_color(&self, token_type: &str) -> &str;
    fn get_reset(&self) -> &str;
}

// Dracula主题
struct DraculaTheme;

impl Theme for DraculaTheme {
    fn get_color(&self, token_type: &str) -> &str {
        match token_type {
            "keyword" => "\x1B[35m",  // 紫色
            "string" => "\x1B[33m",    // 黄色
            "comment" => "\x1B[37m",   // 白色 (灰色)
            "number" => "\x1B[32m",    // 绿色
            "function" => "\x1B[36m",  // 青色
            "class" => "\x1B[34m",     // 蓝色
            _ => "",
        }
    }

    fn get_reset(&self) -> &str {
        "\x1B[0m"
    }
}

// Monokai主题
struct MonokaiTheme;

impl Theme for MonokaiTheme {
    fn get_color(&self, token_type: &str) -> &str {
        match token_type {
            "keyword" => "\x1B[31m",  // 红色
            "string" => "\x1B[33m",    // 黄色
            "comment" => "\x1B[37m",   // 白色 (灰色)
            "number" => "\x1B[32m",    // 绿色
            "function" => "\x1B[36m",  // 青色
            "class" => "\x1B[34m",     // 蓝色
            _ => "",
        }
    }

    fn get_reset(&self) -> &str {
        "\x1B[0m"
    }
}

// 默认主题
struct DefaultTheme;

impl Theme for DefaultTheme {
    fn get_color(&self, token_type: &str) -> &str {
        match token_type {
            "keyword" => "\x1B[33m",  // 黄色
            "string" => "\x1B[32m",    // 绿色
            "comment" => "\x1B[37m",   // 白色 (灰色)
            "number" => "\x1B[31m",    // 红色
            "function" => "\x1B[36m",  // 青色
            "class" => "\x1B[34m",     // 蓝色
            _ => "",
        }
    }

    fn get_reset(&self) -> &str {
        "\x1B[0m"
    }
}

// 语法高亮器
struct SyntaxHighlighter<T: ?Sized + Theme> {
    theme: T,
}

impl<T: ?Sized + Theme> SyntaxHighlighter<T> {
    // 移除ANSI转义序列
    pub fn strip_ansi(&self, text: &str) -> String {
        ANSI_REGEX.replace_all(text, "").to_string()
    }

    // 分割代码块
    pub fn split_blocks<'a>(&self, content: &'a str) -> Vec<HashMap<&'a str, &'a str>> {
        let mut blocks = Vec::new();
        let mut last_end = 0;

        for caps in CODE_BLOCK_REGEX.captures_iter(content) {
            // 添加代码块之前的文本
            if caps.get(0).unwrap().start() > last_end {
                blocks.push(HashMap::from([
                    ("type", "text"),
                    ("content", &content[last_end..caps.get(0).unwrap().start()]),
                ]));
            }

            // 添加代码块
            blocks.push(HashMap::from([
                ("type", "code"),
                ("language", caps.get(1).map_or("", |m| m.as_str())),
                ("content", caps.get(2).map_or("", |m| m.as_str())),
            ]));

            last_end = caps.get(0).unwrap().end();
        }

        // 添加最后一个代码块之后的文本
        if last_end < content.len() {
            blocks.push(HashMap::from([
                ("type", "text"),
                ("content", &content[last_end..]),
            ]));
        }

        blocks
    }

    // 高亮单行代码
    pub fn highlight_line(&self, line: &str) -> String {
        let mut result = String::from(line);

        // 先处理字符串，避免在字符串内的匹配
        let mut string_matches = Vec::new();
        for caps in STRING_REGEX.captures_iter(line) {
            if let Some(m) = caps.get(0) {
                string_matches.push((m.start(), m.end()));
            }
        }

        // 处理注释
        let mut comment_match = None;
        if let Some(caps) = COMMENT_REGEX.captures_iter(line).next() {
            if let Some(m) = caps.get(0) {
                comment_match = Some((m.start(), m.end()));
            }
        }

        // 应用高亮，从最后一个匹配开始替换，避免索引混乱
        let mut replacements = Vec::new();

        // 匹配数字
        for caps in NUMBER_REGEX.captures_iter(line) {
            if let Some(m) = caps.get(0) {
                let start = m.start();
                let end = m.end();
                if !is_inside_string(start, end, &string_matches) && !is_inside_comment(start, end, comment_match) {
                    replacements.push((start, end, self.theme.get_color("number"), self.theme.get_reset()));
                }
            }
        }

        // 匹配函数
        for caps in FUNCTION_REGEX.captures_iter(line) {
            if let Some(m) = caps.get(1) {
                let start = m.start();
                let end = m.end();
                if !is_inside_string(start, end, &string_matches) && !is_inside_comment(start, end, comment_match) {
                    replacements.push((start, end, self.theme.get_color("function"), self.theme.get_reset()));
                }
            }
        }

        // 匹配关键字
        for caps in KEYWORD_REGEX.captures_iter(line) {
            if let Some(m) = caps.get(0) {
                let start = m.start();
                let end = m.end();
                if !is_inside_string(start, end, &string_matches) && !is_inside_comment(start, end, comment_match) {
                    replacements.push((start, end, self.theme.get_color("keyword"), self.theme.get_reset()));
                }
            }
        }

        // 匹配类
        for caps in CLASS_REGEX.captures_iter(line) {
            if let Some(m) = caps.get(1) {
                let start = m.start();
                let end = m.end();
                if !is_inside_string(start, end, &string_matches) && !is_inside_comment(start, end, comment_match) {
                    replacements.push((start, end, self.theme.get_color("class"), self.theme.get_reset()));
                }
            }
        }

        // 匹配字符串
        for (start, end) in string_matches {
            replacements.push((start, end, self.theme.get_color("string"), self.theme.get_reset()));
        }

        // 匹配注释
        if let Some((start, end)) = comment_match {
            replacements.push((start, end, self.theme.get_color("comment"), self.theme.get_reset()));
        }

        // 按开始位置倒序排序
        replacements.sort_by(|a, b| b.0.cmp(&a.0));

        // 应用替换
        for (start, end, color, reset) in replacements {
            let prefix = &result[..start];
            let token = &result[start..end];
            let suffix = &result[end..];
            result = format!("{}{}{}{}{}", prefix, color, token, reset, suffix);
        }

        result
    }

    // 高亮代码块
    pub fn highlight_code(&self, code: &str) -> String {
        let mut highlighted = String::new();
        for line in code.lines() {
            highlighted.push_str(&self.highlight_line(line));
            highlighted.push_str("\n");
        }
        // 移除最后一个换行符
        if !highlighted.is_empty() {
            highlighted.pop();
        }
        highlighted
    }

    // 渲染内容
    pub fn render(&self, content: &str) -> String {
        let blocks = self.split_blocks(content);
        let mut rendered = String::new();

        for block in blocks {
            if block.get("type").unwrap() == &"code" {
                rendered.push_str("```");
                rendered.push_str(block.get("language").unwrap());
                rendered.push_str("\n");
                rendered.push_str(&self.highlight_code(block.get("content").unwrap()));
                rendered.push_str("\n```");
            } else {
                rendered.push_str(block.get("content").unwrap());
            }
        }

        rendered
    }
}

// 辅助函数：检查位置是否在字符串内
fn is_inside_string(start: usize, end: usize, string_matches: &[(usize, usize)]) -> bool {
    for (s, e) in string_matches {
        if start >= *s && end <= *e {
            return true;
        }
    }
    false
}

// 辅助函数：检查位置是否在注释内
fn is_inside_comment(start: usize, end: usize, comment_match: Option<(usize, usize)>) -> bool {
    if let Some((s, e)) = comment_match {
        start >= s && end <= e
    } else {
        false
    }
}

// 创建特定主题的高亮器
fn create_highlighter(theme_name: &str) -> Box<dyn Fn(&str) -> String> {
    match theme_name {
        "dracula" => {
            let highlighter = SyntaxHighlighter { theme: DraculaTheme };
            Box::new(move |content| highlighter.render(content))
        }
        "monokai" => {
            let highlighter = SyntaxHighlighter { theme: MonokaiTheme };
            Box::new(move |content| highlighter.render(content))
        }
        _ => {
            let highlighter = SyntaxHighlighter { theme: DefaultTheme };
            Box::new(move |content| highlighter.render(content))
        }
    }
}

// 公共API函数

// 移除ANSI转义序列
pub fn strip_ansi(text: &str) -> String {
    ANSI_REGEX.replace_all(text, "").to_string()
}

// 分割代码块
pub fn split_blocks(content: &str) -> Vec<HashMap<String, String>> {
    let highlighter = SyntaxHighlighter { theme: DefaultTheme };
    let blocks = highlighter.split_blocks(content);
    // 转换为所有权字符串，避免生命周期问题
    blocks.iter()
        .map(|block| {
            let mut new_block = HashMap::new();
            for (k, v) in block.iter() {
                new_block.insert(k.to_string(), v.to_string());
            }
            new_block
        })
        .collect()
}

// 高亮整个内容
pub fn highlight(content: &str, theme: Option<&str>) -> String {
    let theme_name = theme.unwrap_or("default");
    let render_func = create_highlighter(theme_name);
    render_func(content)
}

// 仅高亮代码
pub fn highlight_code(code: &str, theme: Option<&str>) -> String {
    let theme_name = theme.unwrap_or("default");
    match theme_name {
        "dracula" => {
            let highlighter = SyntaxHighlighter { theme: DraculaTheme };
            highlighter.highlight_code(code)
        }
        "monokai" => {
            let highlighter = SyntaxHighlighter { theme: MonokaiTheme };
            highlighter.highlight_code(code)
        }
        _ => {
            let highlighter = SyntaxHighlighter { theme: DefaultTheme };
            highlighter.highlight_code(code)
        }
    }
}

// Python绑定
#[cfg(feature = "extension-module")]
mod python {
    use super::*;
    use pyo3::prelude::*;

    #[pyfunction]
    unsafe fn strip_ansi_py(text: &str) -> PyResult<String> {
        Ok(strip_ansi(text))
    }

    #[pyfunction]
    unsafe fn highlight_py(content: &str, theme: Option<&str>) -> PyResult<String> {
        Ok(highlight(content, theme))
    }

    #[pyfunction]
    unsafe fn highlight_code_py(code: &str, theme: Option<&str>) -> PyResult<String> {
        Ok(highlight_code(code, theme))
    }

    #[pymodule]
    fn _ds_highlighter(_py: Python, m: &PyModule) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(strip_ansi_py, m)?)?;
        m.add_function(wrap_pyfunction!(highlight_py, m)?)?;
        m.add_function(wrap_pyfunction!(highlight_code_py, m)?)?;
        Ok(())
    }
}

// 测试
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_strip_ansi() {
        let input = "\x1B[31mHello\x1B[0m World";
        let expected = "Hello World";
        assert_eq!(strip_ansi(input), expected);
    }

    #[test]
    fn test_highlight_code() {
        let code = r#"def hello():\n    # This is a comment\n    print("Hello World")\n    return 42"#;
        let highlighted = highlight_code(code, Some("dracula"));
        // 确保高亮后的代码包含ANSI颜色代码
        assert!(highlighted.contains("\x1B[35mdef\x1B[0m"));  // 关键字def被高亮
        assert!(highlighted.contains("\x1B[37m# This is a comment\x1B[0m"));  // 注释被高亮
        assert!(highlighted.contains("\x1B[33m\"Hello World\"\x1B[0m"));  // 字符串被高亮
        assert!(highlighted.contains("\x1B[32m42\x1B[0m"));  // 数字被高亮
    }

    #[test]
    fn test_highlight() {
        let content = r#"Some text\n```python\ndef hello():\n    print("Hello")\n```\nMore text"#;
        let highlighted = highlight(content, Some("monokai"));
        // 确保代码块被高亮，而普通文本保持不变
        assert!(highlighted.contains("Some text"));
        assert!(highlighted.contains("\x1B[31mdef\x1B[0m"));  // 关键字def被高亮
        assert!(highlighted.contains("More text"));
    }
}
