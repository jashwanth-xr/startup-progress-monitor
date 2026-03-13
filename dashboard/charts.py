import plotly.express as px


def revenue_chart(df):
    fig = px.line(
        df,
        x="month",
        y="revenue",
        title="Revenue Growth"
    )
    return fig


def user_chart(df):
    fig = px.line(
        df,
        x="month",
        y="users",
        title="User Growth"
    )
    return fig


def burn_chart(df):
    fig = px.line(
        df,
        x="month",
        y="burn_rate",
        title="Burn Rate"
    )
    return fig


def momentum_chart(compare_df):

    import plotly.express as px

    fig = px.scatter(
        compare_df,
        x="growth",
        y="burn",
        text="startup",
        color="startup",
        size=[20]*len(compare_df),
        title="Startup Momentum vs Burn Rate",
        hover_data=["growth","burn"]
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(
            line=dict(width=2, color="white")
        )
    )

    fig.update_layout(
        xaxis_title="Growth Momentum",
        yaxis_title="Burn Rate",
        showlegend=False
    )

    return fig
