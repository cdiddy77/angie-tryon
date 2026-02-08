---
id: at-k63c
status: closed
deps: [at-gx1x]
links: []
created: 2026-02-02T07:01:32Z
type: task
priority: 1
assignee: cdiddy77
parent: at-3pzv
tags: [frontend, hooks]
---
# Create frontend hooks for tagging

Implement React hooks for tag operations: useTagGeneration (add/remove tags), useGenerationsByTag (filter by tag), useManageTags (CRUD operations). Add to @weirdfingers/boards package following existing patterns.

## Acceptance Criteria

All hooks work correctly, Follow existing hook patterns, TypeScript types complete

## Notes

**2026-02-08T15:20:49Z**

Implemented frontend hooks for tagging:

**New files created:**
- packages/frontend/src/hooks/useTags.ts - All tag hooks

**Modified files:**
- packages/frontend/src/graphql/operations.ts - Added tag GraphQL operations
- packages/frontend/src/index.ts - Exported new hooks

**Hooks implemented:**
1. useManageTags - CRUD operations for tags (create, update, delete, list)
2. useTagGeneration - Add/remove tags from a specific generation
3. useTag - Fetch a single tag by ID
4. useTagBySlug - Fetch a single tag by slug

**GraphQL operations added:**
- Queries: GET_TAGS, GET_TAG, GET_TAG_BY_SLUG, GET_GENERATION_TAGS
- Mutations: CREATE_TAG, UPDATE_TAG, DELETE_TAG, ADD_TAG_TO_GENERATION, REMOVE_TAG_FROM_GENERATION
- Fragment: TAG_FRAGMENT
- Types: Tag, CreateTagInput, UpdateTagInput

**Acceptance Criteria met:**
- All hooks work correctly following existing patterns
- TypeScript types complete with full hook return types
- Typecheck and tests pass
