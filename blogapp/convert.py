import markdown
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from pymdownx import superfences, magiclink, caret, betterem, mark, tasklist, tilde, emoji, inlinehilite, critic, highlight, \
    _bypassnorm
import mdx_math

extensions = [
    'markdown.extensions.abbr',
    'markdown.extensions.attr_list',
    'markdown.extensions.def_list',
    'markdown.extensions.fenced_code',
    'markdown.extensions.footnotes',
    'markdown.extensions.md_in_html',
    'markdown.extensions.tables',
    'markdown.extensions.codehilite',
    'markdown.extensions.legacy_em',
    TocExtension(slugify=slugify),
    'markdown.extensions.wikilinks',
    'markdown.extensions.admonition',
    'markdown.extensions.legacy_attrs',
    'markdown.extensions.meta',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    'markdown.extensions.smarty',
    'mdx_math',  # KaTeX数学公式，$E=mc^2$和$$E=mc^2$$
    # 'markdown_checklist.extension',  # checklist，- [ ]和- [x]
    'pymdownx.magiclink',  # 自动转超链接，
    'pymdownx.caret',  # 上标下标，
    'pymdownx.superfences',  # 多种块功能允许嵌套，各种图表
    'pymdownx.betterem',  # 改善强调的处理(粗体和斜体)
    'pymdownx.mark',  # 亮色突出文本
    'pymdownx.highlight',  # 高亮显示代码
    'pymdownx.tasklist',  # 任务列表
    'pymdownx.tilde',  # 删除线
    'pymdownx.emoji',
    'pymdownx.inlinehilite',
    # 'pymdownx.arithmatex',
    'pymdownx.critic',
    # 'markdown_markup_emoji.markup_emoji',
]
extension_configs = {
    'mdx_math': {
        'enable_dollar_delimiter': True  # 允许单个$
    },
    'pymdownx.superfences': {
        "custom_fences": [
            {
                'name': 'mermaid',  # 开启流程图等图
                'class': 'mermaid',
                'format': superfences.fence_div_format
            }
        ]
    },
    'pymdownx.highlight': {
        'linenums': True,  # 显示行号
        'linenums_style': 'pymdownx-inline'  # 代码和行号分开
    },
    'pymdownx.tasklist': {
        'clickable_checkbox': True,  # 任务列表可点击
    }
}  # 扩展配置


def md2html(text):
    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)
    html = md.convert(text)
    return html, md.toc


def getOutline(text):
    return ""
