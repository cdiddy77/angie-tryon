---
id: at-gx1x
status: closed
deps: [at-e77m]
links: []
created: 2026-02-02T07:00:07Z
type: task
priority: 0
assignee: cdiddy77
parent: at-3pzv
tags: [backend, graphql]
---
# Add tagging to GraphQL schema

Add tag types to GraphQL schema using Strawberry. Create mutations for tagging generations (addTag, removeTag). Add tag filtering to generation queries. Include tags in generation responses.

## Acceptance Criteria

Tag types in GraphQL schema, Mutations work for adding/removing tags, Can query generations by tag

## Notes

**2026-02-04T20:51:50Z**

Completed implementation of tagging in GraphQL schema:

**New files created:**
- `packages/backend/src/boards/graphql/types/tag.py` - Tag GraphQL type with conversion function
- `packages/backend/src/boards/graphql/resolvers/tag.py` - All tag resolvers (CRUD + generation tagging)

**Modified files:**
- `packages/backend/src/boards/graphql/mutations/root.py` - Added tag mutations (createTag, updateTag, deleteTag, addTagToGeneration, removeTagFromGeneration)
- `packages/backend/src/boards/graphql/queries/root.py` - Added tag queries (tags, tag, tagBySlug)
- `packages/backend/src/boards/graphql/types/generation.py` - Added tags field to Generation type

**GraphQL Schema additions:**
- Tag type with fields: id, tenant_id, name, slug, description, metadata, created_at, updated_at
- Queries: tags, tag(id), tagBySlug(slug)
- Mutations: createTag, updateTag, deleteTag, addTagToGeneration, removeTagFromGeneration
- Generation.tags field for querying tags on generations

**Features:**
- Auto-generated slugs from tag names
- Tenant-scoped tags with unique slug per tenant
- Board access control for tagging generations (owner/editor required)
- All acceptance criteria met: Tag types in GraphQL schema, Mutations work for adding/removing tags, Can query generations by tag

Typecheck and tests pass (1593 tests passed).
