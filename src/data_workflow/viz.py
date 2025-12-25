from pathlib import Path
import plotly.express as px
import pandas as pd

def bar_sorted(df: pd.DataFrame, x: str, y: str, title: str) -> None:
    dfSorted = df.sort_values(y , ascending=False)
    fig = px.bar(dfSorted, x=x, y=y, title=title)
    fig.update_layout(
        title={"x": 0.02},
        margin={"l": 60, "r": 20, "t": 60, "b": 60},
    )
    fig.update_xaxes(title_text=x)
    fig.update_yaxes(title_text=y)
    return fig

def time_line(df: pd.DataFrame, x: str, y: str, color=None, title: str = "") :
    dfsorted = df.sort_values(by = x )
    fig = px.line(dfsorted, x=x, y=y, color=color, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)

    return fig

def histogram_chart(df, x: str, nbins: int = 30, title: str = ""):
    fig = px.histogram(df, x=x, nbins=nbins, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title="count of oreders")
    return fig

def save_fig(fig, path: Path, scale: int =2) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(str(path) , scale=scale)