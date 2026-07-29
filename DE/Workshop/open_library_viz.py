import marimo

__generated_with = "0.20.1"
app = marimo.App()

with app.setup:
    import marimo
    import dlt
    import ibis
    import altair as alt


@app.cell
def _():
    # 1. Pipeline and Ibis connection
    pipeline = dlt.pipeline(
        pipeline_name="open_library_pipeline",
        destination="duckdb",
        dataset_name="open_library_data",
    )
    dataset = pipeline.dataset()
    ibis_conn = dataset.ibis()
    return (ibis_conn,)


@app.cell
def _(ibis_conn):
    # 2. Top 10 authors by work_count
    authors_table = ibis_conn.table("authors", database="open_library_data")
    top10_authors = (
        authors_table.select("name", "work_count")
        .order_by(ibis.desc("work_count"))
        .limit(10)
    )
    df_top10 = top10_authors.to_pandas()
    return (df_top10,)


@app.cell
def _(df_top10):
    # Table preview
    marimo.ui.table(df_top10)
    return


@app.cell
def _(df_top10):
    # 3. Altair bar chart
    chart = (
        alt.Chart(df_top10)
        .mark_bar()
        .encode(
            x=alt.X("work_count", title="work_count"),
            y=alt.Y("name", title="Author", sort="-x"),
            tooltip=["name", "work_count"],
        )
        .properties(
            title="Top 10 authors by work_count",
            width=600,
            height=400,
        )
    )
    chart
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
