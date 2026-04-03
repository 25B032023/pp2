CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_surname VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE name = p_name AND surname = p_surname
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name AND surname = p_surname;
    ELSE
        INSERT INTO phonebook(name, surname, phone)
        VALUES (p_name, p_surname, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_surnames VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_names, 1)
    LOOP
        IF p_phones[i] ~ '^87[0-9]{9}$' THEN
            INSERT INTO phonebook(name, surname, phone)
            VALUES (p_names[i], p_surnames[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Incorrect phone: %, %, %',
                p_names[i], p_surnames[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value
       OR phone = p_value;
END;
$$;