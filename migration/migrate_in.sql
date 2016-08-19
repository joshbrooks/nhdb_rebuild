BEGIN TRANSACTION;
-- TRUNCATE project_tracker_project CASCADE;
-- COPY project_tracker_project (id, name, description, startdate, enddate, verified, fulltimestaff, parttimestaff, status) FROM '/tmp/tables/project.tab';
-- COPY project_tracker_organization (id, name, type, active, fulltimestaff, parttimestaff, verified) FROM '/tmp/tables/organization.tab';
-- COPY project_tracker_person (id, name, title, organization_id) FROM '/tmp/tables/person.tab';
-- COPY jsontag_translation (object_id, content_type_id, translation) FROM '/tmp/tables/objecttranslation.tab';
-- COPY jsontag_tag(object_id, "group", translation_id) FROM '/tmp/tables/tag.tab';
-- COPY jsontag_objecttag(object_id, content_type_id, tag_id_id) FROM '/tmp/tables/objecttag.tab';
-- TRUNCATE project_tracker_person CASCADE;
-- COPY project_tracker_person(id, organization_id, name, title, modified, verified) FROM '/tmp/tables/export.person.tab';
-- COPY project_tracker_projectperson(id, person_id, project_id, relationship, verified) FROM '/tmp/tables/export.projectperson.tab';
COPY project_tracker_projectorganization(id, project_id, organization_id, projectorganization) FROM '/tmp/tables/export.project_organization.tab';
END TRANSACTION
