from datasette.app import Datasette
import pytest
import pytest_asyncio

FRAGMENT = '</html>\n<script>\nlet footer = document.querySelector("footer");'


@pytest_asyncio.fixture
async def ds():
    datasette = Datasette([], memory=True)
    db = datasette.add_memory_database("db")
    if not await db.table_exists("t"):
        await db.execute_write("create table t (id integer primary key)")
        await db.execute_write("insert into t (id) values (1)")
    return datasette


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ("/", "/db", "/db/t", "/db/t/1"))
async def test_plugin_affects_pages(ds, path):
    response = await ds.client.get(path)
    assert response.status_code == 200
    assert FRAGMENT in response.text


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "path", ("/.json", "/db.json", "/db/t.json", "/db/t.csv", "/db/t/1.json")
)
async def test_plugin_does_not_affect_non_html(ds, path):
    response = await ds.client.get(path)
    assert response.status_code == 200
    assert FRAGMENT not in response.text
