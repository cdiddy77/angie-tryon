---
id: at-e77m
status: closed
deps: []
links: []
created: 2026-02-02T07:00:00Z
type: task
priority: 0
assignee: cdiddy77
parent: at-3pzv
tags: [backend, database]
---
# Create tag data model for boards

Design and implement many-to-many relationship between generations and tags. Add Tag model to SQLAlchemy. Create database migration. Tags will categorize wardrobe items (model, top, bottom, shoes, etc).

## Acceptance Criteria

Tag model created in SQLAlchemy, Migration runs successfully, Many-to-many relationship works


## Notes

**2026-02-04T15:34:24Z**

Completed implementation of tag data model:

- Created Tags model in SQLAlchemy with fields: id, tenant_id, name, slug, description, metadata, created_at, updated_at
- Created GenerationTags association table for many-to-many relationship between generations and tags
- Added relationships to existing models (Tenants, Generations)
- Created and applied Alembic migration (revision: b2fe3780f8c0)
- Tested functionality with sample wardrobe tags (model, top, bottom, shoes, accessories)
- All acceptance criteria met: Tag model created, migration runs successfully, many-to-many relationship works correctly

Files modified:
- /packages/backend/src/boards/dbmodels/__init__.py (added Tags and GenerationTags models)
- /packages/backend/src/boards/database/models.py (updated exports)
- /packages/backend/alembic/versions/202624_7309_add_tags_and_generation_tags_tables_for_.py (new migration)

Ready for GraphQL schema integration (ticket at-gx1x)
