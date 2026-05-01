DROP PROCEDURE IF EXISTS add_phone(VARCHAR, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS move_to_group(VARCHAR, VARCHAR);
DROP FUNCTION IF EXISTS search_contacts(TEXT);

CREATE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    contact_id_var INT;
BEGIN
    SELECT id
    INTO contact_id_var
    FROM contacts
    WHERE name = p_contact_name;

    INSERT INTO phones(contact_id, phone, phone_type)
    VALUES (contact_id_var, p_phone, p_type);
END;
$$;


CREATE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    group_id_var INT;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO group_id_var
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = group_id_var
    WHERE name = p_contact_name;
END;
$$;


CREATE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    contact_id INT,
    contact_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name,
        p.phone,
        p.phone_type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR g.name ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;