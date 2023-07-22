CREATE TABLE IF NOT EXISTS public.reader (
    reader_id serial PRIMARY KEY,
    ticket_num BIGINT NOT NULL,
    full_name varchar(255) NOT NULL,
    address_reader varchar(255) NOT NULL,
    num_phone varchar(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.book (
    book_id serial PRIMARY KEY,
    cipher_book varchar(20) NOT NULL,
    title varchar(255) NOT NULL,
    year_public smallint NOT NULL,
    volume_pages integer,
    price numeric(7, 2) NOT NULL DEFAULT 0,
    count_instances integer NOT NULL DEFAULT 0,
    publish_house varchar(255)
);

CREATE TABLE IF NOT EXISTS public.reader_book (
    reader_book_id serial PRIMARY KEY,
    reader_id BIGINT REFERENCES public.reader (reader_id) ON DELETE CASCADE,
    book_id BIGINT REFERENCES public.book (book_id) ON DELETE CASCADE,
    date_receipt date NOT NULL DEFAULT CURRENT_DATE,
    date_return date
);