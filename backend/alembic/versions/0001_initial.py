"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-21
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "movies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "analysis_jobs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("query", sa.String(length=512), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("result", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("movie_id", sa.Integer(), sa.ForeignKey("movies.id"), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("source_url", sa.String(length=1024), nullable=True),
        sa.Column("author", sa.String(length=256), nullable=True),
        sa.Column("language", sa.String(length=16), nullable=False),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("posted_at", sa.DateTime(), nullable=True),
        sa.Column("fake_probability", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "review_embeddings",
        sa.Column("review_id", sa.Integer(), sa.ForeignKey("reviews.id"), primary_key=True),
        sa.Column("embedding", Vector(384), nullable=False),
    )
    op.create_table(
        "platform_reports",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("job_id", sa.Integer(), sa.ForeignKey("analysis_jobs.id"), nullable=False),
        sa.Column("platform", sa.String(length=64), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_review_embeddings_hnsw ON review_embeddings USING hnsw (embedding vector_cosine_ops)")


def downgrade() -> None:
    op.drop_table("platform_reports")
    op.drop_table("review_embeddings")
    op.drop_table("reviews")
    op.drop_table("analysis_jobs")
    op.drop_table("movies")
