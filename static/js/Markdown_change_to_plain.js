document.addEventListener('DOMContentLoaded', function () {
    var markdownContentElements = document.querySelectorAll('.markdownContent_to_change');

    markdownContentElements.forEach(function (markdownContentElement) {
        var markdownContent = markdownContentElement.innerHTML;
        console.log('Markdown Content:', markdownContent);

        // 移除 Markdown 格式
        var plainText = markdownContent
            .replace(/^[\*\-+]\s+/gm, '') // 移除列表符号
            .replace(/^(#+)\s+(.*)/gm, '$2') // 移除标题
            .replace(/(\*\*|__|\*|_|\~\~|`{1,3})/g, '') // 移除加粗、斜体、删除线、内联代码块
            .replace(/\!\[.*?\]\(.*?\)/g, '') // 移除图片语法
            .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // 移除链接语法
            .replace(/(&gt;|\>)(.*)/g, '') // 移除引用
            .replace(/(`{3})([\s\S]*?)(`{3})/g, '') // 移除代码块
            .replace(/\s+/g, ''); // 移除空白字符

        // 截取前 50 个字符
        var truncatedText = plainText.slice(0, 50);
        console.log('Truncated Text:', truncatedText);

        // 创建一个新的元素来显示结果
        var resultDisplayElement = document.createElement('div');
        resultDisplayElement.textContent = truncatedText;

        // 替换原始内容
        markdownContentElement.parentNode.replaceChild(resultDisplayElement, markdownContentElement);
    });
});