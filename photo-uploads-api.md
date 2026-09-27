# Photo Upload API

The API accepts photos one file per request, grouped into upload batches. The
batch status endpoint reports uploaded, in-progress, and expected file counts.

## Limits and storage

- A batch can contain at most 5,000 files.
- Each file can be at most 25 MiB (26,214,400 bytes).
- Accepted filename extensions are `.jpg`, `.jpeg`, `.png`, `.webp`, and `.gif`.
- The request media type must be an image media type or
  `application/octet-stream`.
- Files are written in 1 MiB chunks, using server-generated names. The original
  client filename is metadata only and is not used as a disk path.
- Files are stored directly under `uploads/properties-photos/`, with globally
  unique server-generated filenames. Batch and file metadata is kept in
  `.photo_uploads.sqlite3` under the same upload root.
- Docker Compose mounts a persistent named volume at `/app/uploads`.

## Create a batch

`POST /api/v1/photos/batches`

The request body is optional. Supply `expected_files` when the caller knows the
total; it enables percentage progress and prevents uploading more than the
declared count.

```http
POST /api/v1/photos/batches
Content-Type: application/json

{"expected_files": 5000}
```

Response: `201 Created`

```json
{
  "batch_id": "d8cb08c1-1896-4d6a-856b-e3eaf87b9cf1",
  "status": "open",
  "expected_files": 5000,
  "created_at": "2026-09-28T12:00:00+00:00"
}
```

## Upload a photo

`POST /api/v1/photos/batches/{batch_id}/files`

Send one multipart file in the `file` field. The server streams it to a
temporary file and moves it into its final location after the upload succeeds.

```bash
curl -X POST "http://localhost:8000/api/v1/photos/batches/$BATCH_ID/files" \
  -F "file=@property-front.jpg;type=image/jpeg"
```

Response: `201 Created`

```json
{
  "file_id": "eb8cd769-964d-4b19-8025-4641f74a4d0d",
  "batch_id": "d8cb08c1-1896-4d6a-856b-e3eaf87b9cf1",
  "filename": "property-front.jpg",
  "mime_type": "image/jpeg",
  "size_bytes": 482731,
  "path": "uploads/properties-photos/eb8cd769-964d-4b19-8025-4641f74a4d0d.jpg"
}
```

Persist the returned `path` in `AccountsPhotos.ImagePath` so the photo can be
located without batch metadata. The batch relationship remains tracked by the
upload API and does not affect the image path.

## Read batch progress

`GET /api/v1/photos/batches/{batch_id}`

Response: `200 OK`

```json
{
  "batch_id": "d8cb08c1-1896-4d6a-856b-e3eaf87b9cf1",
  "status": "open",
  "expected_files": 5000,
  "total_files": 120,
  "uploaded_files": 119,
  "uploading_files": 1,
  "progress_percent": 2.38,
  "created_at": "2026-09-28T12:00:00+00:00",
  "completed_at": null
}
```

`progress_percent` is `null` if the batch was created without `expected_files`.
In that case, use the file counts to track progress.

## Complete a batch

`POST /api/v1/photos/batches/{batch_id}/complete`

No request body is required. A batch can be completed when it has at least one
successfully uploaded file and no uploads in progress. If `expected_files` was
declared, all expected files must have uploaded. Completing an already
completed batch is idempotent.

Response: `200 OK`

```json
{
  "batch_id": "d8cb08c1-1896-4d6a-856b-e3eaf87b9cf1",
  "status": "completed",
  "completed_at": "2026-09-28T12:30:00+00:00"
}
```

## Errors

Errors use FastAPI's standard JSON shape, for example `{"detail":"..."}`.

| Status | Meaning |
| --- | --- |
| `400` | The uploaded file is empty. |
| `404` | The batch ID does not exist. |
| `409` | The batch is complete, its file limit was reached, uploads remain in progress, or completion requirements are unmet. |
| `413` | The photo exceeds the per-file size limit. |
| `415` | The file extension or media type is unsupported. |
| `422` | Request validation failed, including an invalid `expected_files` value. |