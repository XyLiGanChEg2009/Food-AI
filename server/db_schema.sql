--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: foodcard; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.foodcard (
    id integer NOT NULL,
    img_src text NOT NULL,
    price integer NOT NULL,
    weight integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.foodcard OWNER TO postgres;

--
-- Name: foodcard_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.foodcard_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.foodcard_id_seq OWNER TO postgres;

--
-- Name: foodcard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.foodcard_id_seq OWNED BY public.foodcard.id;


--
-- Name: foodcard id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foodcard ALTER COLUMN id SET DEFAULT nextval('public.foodcard_id_seq'::regclass);


--
-- Name: foodcard foodcard_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foodcard
    ADD CONSTRAINT foodcard_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

