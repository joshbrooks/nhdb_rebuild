CREATE TEMP TABLE objecttag (
  object_id       UUID PRIMARY KEY,
  content_type_id        UUID ,
  tag  JSON
);
DROP TABLE jsontag_tag;
CREATE TEMP TABLE jsontag_tag
(
    object_id UUID PRIMARY KEY NOT NULL,
    "group" VARCHAR(255) NOT NULL,
    translation_id UUID
);

CREATE TEMP TABLE objecttranslations
(
    object_id UUID PRIMARY KEY,
    translation JSONB,
    content_type_id INTEGER
);

INSERT INTO objecttranslations(object_id, content_type_id) SELECT uuid, 18 FROM nhdb_propertytag;
UPDATE objecttranslations
SET translation = (
  SELECT row_to_json(r)
  FROM (SELECT
          name AS name_en,
          name_tet,
          name_pt,
          name_ind,
          description_en,
          description_tet,
          description_pt,
          description_ind
        FROM nhdb_propertytag
        WHERE uuid = objecttranslations.object_id)
    AS r)
WHERE object_id IN (SELECT uuid
             FROM nhdb_propertytag);

SELECT * FROM objecttranslations;

INSERT INTO jsontag_tag(object_id, "group", translation_id)
SELECT nhdb_propertytag.uuid, SUBSTRING(nhdb_propertytag.path FOR 3), objecttranslations.object_id
FROM nhdb_propertytag, objecttranslations WHERE nhdb_propertytag.uuid = objecttranslations.object_id;
)

SELECT * FROM objecttranslations;

SELECT * FROM jsontag_tag t, objecttranslations tr WHERE t.object_id = tr.object_id;

INSERT INTO objecttag (object_id, content_type_id, tag)
SELECT
  nhdb_project.uuid,
  11,
  nhdb_propertytag.uuid
FROM
  (SELECT * FROM nhdb_project_activity
   UNION SELECT * FROM nhdb_project_beneficiary
   UNION SELECT * FROM nhdb_project_sector)
          AS project_tags, nhdb_project, nhdb_propertytag
  WHERE project_id = nhdb_project.id
  AND nhdb_propertytag.id = project_tags.propertytag_id;

