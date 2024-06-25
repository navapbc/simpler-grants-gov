#
# Unit tests for src.data_migration.load.sql.
#

import pytest
import sqlalchemy

from src.data_migration.load import sql


@pytest.fixture(scope="module")
def sqlalchemy_metadata():
    return sqlalchemy.MetaData()


@pytest.fixture(scope="module")
def source_table(sqlalchemy_metadata):
    return sqlalchemy.Table(
        "test_source_table",
        sqlalchemy_metadata,
        sqlalchemy.Column("id1", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("id2", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("x", sqlalchemy.Text),
        sqlalchemy.Column("last_upd_date", sqlalchemy.TIMESTAMP),
    )


@pytest.fixture(scope="module")
def destination_table(sqlalchemy_metadata):
    return sqlalchemy.Table(
        "test_destination_table",
        sqlalchemy_metadata,
        sqlalchemy.Column("id1", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("id2", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("x", sqlalchemy.Text),
        sqlalchemy.Column("is_deleted", sqlalchemy.Boolean),
        sqlalchemy.Column("last_upd_date", sqlalchemy.TIMESTAMP),
    )


def test_build_select_new_rows_sql(source_table, destination_table):
    select = sql.build_select_new_rows_sql(source_table, destination_table)
    assert str(select) == (
        "SELECT test_source_table.id1, test_source_table.id2 \n"
        "FROM test_source_table \n"
        "WHERE ((test_source_table.id1, test_source_table.id2) "
        "NOT IN ("
        "SELECT test_destination_table.id1, test_destination_table.id2 \n"
        "FROM test_destination_table)) "
        "ORDER BY test_source_table.id1, test_source_table.id2"
    )


def test_build_select_updated_rows_sql(source_table, destination_table):
    select = sql.build_select_updated_rows_sql(source_table, destination_table)
    assert str(select) == (
        "SELECT test_destination_table.id1, test_destination_table.id2 \n"
        "FROM test_destination_table "
        "JOIN test_source_table ON "
        "(test_destination_table.id1, test_destination_table.id2) = "
        "(test_source_table.id1, test_source_table.id2) \n"
        "WHERE test_destination_table.last_upd_date < test_source_table.last_upd_date "
        "ORDER BY test_source_table.id1, test_source_table.id2"
    )


def test_build_insert_select_sql(source_table, destination_table):
    insert = sql.build_insert_select_sql(source_table, destination_table, [(1, 2), (3, 4), (5, 6)])
    assert str(insert) == (
        "INSERT INTO test_destination_table (id1, id2, x, last_upd_date, is_deleted) "
        "SELECT test_source_table.id1, test_source_table.id2, test_source_table.x, "
        "test_source_table.last_upd_date, FALSE AS is_deleted \n"
        "FROM test_source_table \n"
        "WHERE (test_source_table.id1, test_source_table.id2) IN (__[POSTCOMPILE_param_1])"
    )


def test_build_update_sql(source_table, destination_table):
    update = sql.build_update_sql(source_table, destination_table, [(1, 2), (3, 4), (5, 6)])
    assert str(update) == (
        "UPDATE test_destination_table "
        "SET id1=test_source_table.id1, id2=test_source_table.id2, x=test_source_table.x, "
        "last_upd_date=test_source_table.last_upd_date FROM test_source_table "
        "WHERE (test_destination_table.id1, test_destination_table.id2) = "
        "(test_source_table.id1, test_source_table.id2) AND "
        "(test_source_table.id1, test_source_table.id2) "
        "IN (__[POSTCOMPILE_param_1])"
    )


def test_build_mark_deleted_sql(source_table, destination_table):
    update = sql.build_mark_deleted_sql(source_table, destination_table)
    assert str(update) == (
        "UPDATE test_destination_table "
        "SET is_deleted=:is_deleted "
        "WHERE test_destination_table.is_deleted = false "
        "AND ((test_destination_table.id1, test_destination_table.id2) "
        "NOT IN (SELECT test_source_table.id1, test_source_table.id2 \n"
        "FROM test_source_table))"
    )
