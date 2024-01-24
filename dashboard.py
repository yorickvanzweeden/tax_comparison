import re
from typing import Callable

from bokeh.layouts import row
from bokeh.models import ColumnDataSource, CustomJS, CheckboxGroup, LabelSet
from bokeh.models import TabPanel, Tabs, NumeralTickFormatter, HoverTool
from bokeh.plotting import figure
from pydantic import BaseModel

from calculations.box1 import belasting_box_1
from calculations.box1_werknemer import belasting_box_1_werknemer
from calculations.zorgtoeslag import calculate_zorgtoeslag


class Category(BaseModel):
    label: str
    color: str | None = None
    data: list
    width: int = 4
    line_dash: str = "solid"
    shown: bool = True
    new_section: bool = False
    format: Callable[[str], str] = lambda x: f"€@{x}{{0,0}}"
    key_extra: str | None = None
    header: str | None = None

    @property
    def key(self):
        return re.sub(r'[ -()+]', '', self.label) + (self.key_extra or "")


def get_formatter():
    return NumeralTickFormatter(format="€0,0")


def create_tax_chart(salary_range, categories):
    p = figure(width=1200, height=600)
    p.xaxis[0].formatter = get_formatter()
    p.yaxis[0].formatter = get_formatter()
    p.xaxis[0].axis_label = 'Bruto jaarinkomen (€)'
    p.yaxis[0].axis_label = 'Netto salaris (€)'

    source = ColumnDataSource(data={"x": salary_range} | {category.key: category.data for category in categories})
    lines = [p.line('x', category.key, source=source, line_color=category.color, line_width=category.width,
                    line_dash=category.line_dash) for category in categories if category.shown]

    tooltips = """
    <div>
        <div>
            <table style="width:100%;font-size:14px;">
    """

    for category in categories:
        tooltips += f"""
                {f'<tr><td colspan="2" style="border-bottom: 1px solid black;padding: {20 if category.new_section else 0} 0 0 0;"><strong>' + category.header + '</strong></td></tr>' if category.header else ''}
                <tr style="font-size: {10 if category.width == 2 else 14}px">
                    <td style="padding:0px 10px 0 5px;">
                        <strong>{category.label}</strong>
                    </td>
                    <td style="padding:0px 10px 0 10px; text-align:right;
                    font-weight: {'normal' if category.width == 2 else 'bold'}">
                        {category.format(category.key)}
                    </td>
                </tr>
        """

    tooltips += f"""
            </table>
        </div>
    </div>
    """
    hover_tool = HoverTool(renderers=[lines[5]], mode='vline', tooltips=tooltips)
    p.add_tools(hover_tool)

    return p, lines


def dashboard(doc):
    salary_range = list(range(1, 120_000, 10))
    categories = [Category(label="Bruto jaarinkomen", color="steelblue", data=salary_range,
                           width=1, line_dash="dotted"),
                  Category(label="Per maand (bruto)", shown=False, data=[sal / 12 for sal in salary_range],
                           width=2),

                  Category(label="+ Box 1", color="firebrick", new_section=True, header="Ondernemer", width=2,
                           data=[belasting_box_1(sal, False, False, False) for sal in salary_range]),
                  Category(label="+ MKB vrijstelling", color="lightpink", width=2,
                           data=[belasting_box_1(sal, True, False, False) for sal in salary_range]),
                  Category(label="+ Zelfstandigenaftrek", color="lightcoral", width=2,
                           data=[belasting_box_1(sal, True, True, False) for sal in salary_range]),
                  Category(label="+ WBSO", color="orangered", width=2,
                           data=[belasting_box_1(sal, True, True, True) for sal in salary_range]),
                  Category(label="+ Zorgtoeslag", color="red", width=2,
                           data=[belasting_box_1(sal, True, True, True) + calculate_zorgtoeslag(sal) for sal in
                                 salary_range]),

                  Category(label="Per maand (netto)", new_section=True, shown=False,
                           data=[(belasting_box_1(sal, True, True, True) + calculate_zorgtoeslag(sal)) / 12 for sal in
                                 salary_range]),

                  Category(label="+ Box 1", key_extra="wn", new_section=True, color="limegreen", header="Werknemer",
                           width=2,
                           data=[belasting_box_1_werknemer(sal) for sal in salary_range]),
                  Category(label="+ vakantietoeslag", width=2, color="lightgreen",
                           data=[belasting_box_1_werknemer(sal, True) for sal in salary_range]),
                  Category(label="+ 13e maand", width=2, color="olivedrab",
                           data=[belasting_box_1_werknemer(sal, True, True) for sal in salary_range]),
                  Category(label="+ Zorgtoeslag", key_extra="wn", color="green", width=2,
                           data=[belasting_box_1_werknemer(sal, True, True) + calculate_zorgtoeslag(sal) for sal in
                                 salary_range]),
                  Category(label="Per maand (netto)", key_extra="wn", new_section=True, shown=False,
                           data=[(belasting_box_1_werknemer(sal, True, True) + calculate_zorgtoeslag(sal)) / 12 for sal
                                 in salary_range]),
                  ]

    plot, lines = create_tax_chart(salary_range, categories)

    netto_targets = [36000, 48000, 60000]
    bruto_reqs = [36487, 59786, 86127]

    source = ColumnDataSource(data=dict(x=[0, 0, 0] + bruto_reqs, y=netto_targets + [0, 0, 0],
                                        names=['3K per maand', '4K per maand', '5K per maand'] + [f"€{x:,}" for x in bruto_reqs]))
    labels = LabelSet(x='x', y='y', text='names', x_offset=5, y_offset=5, source=source)
    plot.add_layout(labels)

    # Add lines for 3K per month, 4K per month, etc.
    for y in netto_targets:
        plot.line(salary_range, [y for _ in salary_range], line_color="black", line_dash="dashed", width=2)
    for x in bruto_reqs:
        plot.line([x for _ in salary_range], salary_range, line_color="black", line_dash="dashed", width=2)
    plot.line([45_000 for _ in salary_range], salary_range, line_color="red", line_dash="dashed", width=2)

    checkbox_group = CheckboxGroup(labels=[category.label for category in categories if category.shown],
                                   active=[i for i, category in enumerate(categories) if category.shown])

    checkbox_group.js_on_change("active", CustomJS(args=dict(lines=lines, checkbox_group=checkbox_group), code="""
        for (var i = 0; i < lines.length; i++) {
            lines[i].visible = checkbox_group.active.includes(i);
        }
    """))

    tab1 = TabPanel(child=row(checkbox_group, plot), title="Belasting Box 1 (ondernemer)")
    tabs = Tabs(tabs=[tab1])
    doc.add_root(tabs)
