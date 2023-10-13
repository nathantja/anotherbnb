--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Homebrew)
-- Dumped by pg_dump version 15.3 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_user_id_fkey;
ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_listing_id_fkey;
ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_sender_user_id_fkey;
ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_recipient_user_id_fkey;
ALTER TABLE ONLY public.listings DROP CONSTRAINT listings_user_id_fkey;
ALTER TABLE ONLY public.images DROP CONSTRAINT images_listing_id_fkey;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_username_key;
ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.reservations DROP CONSTRAINT reservations_pkey;
ALTER TABLE ONLY public.messages DROP CONSTRAINT messages_pkey;
ALTER TABLE ONLY public.listings DROP CONSTRAINT listings_pkey;
ALTER TABLE ONLY public.images DROP CONSTRAINT images_pkey;
ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.reservations ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.messages ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.listings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.images ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.users_id_seq;
DROP TABLE public.users;
DROP SEQUENCE public.reservations_id_seq;
DROP TABLE public.reservations;
DROP SEQUENCE public.messages_id_seq;
DROP TABLE public.messages;
DROP SEQUENCE public.listings_id_seq;
DROP TABLE public.listings;
DROP SEQUENCE public.images_id_seq;
DROP TABLE public.images;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: images; Type: TABLE; Schema: public; Owner: nathantjahjadi
--

CREATE TABLE public.images (
    id integer NOT NULL,
    listing_id integer NOT NULL,
    original_filename character varying(255) NOT NULL,
    filename character varying(255) NOT NULL,
    url character varying(1000) NOT NULL
);


ALTER TABLE public.images OWNER TO nathantjahjadi;

--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: nathantjahjadi
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.images_id_seq OWNER TO nathantjahjadi;

--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nathantjahjadi
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: listings; Type: TABLE; Schema: public; Owner: nathantjahjadi
--

CREATE TABLE public.listings (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(30) NOT NULL,
    description character varying(1000) NOT NULL,
    sq_ft integer NOT NULL,
    max_guests integer NOT NULL,
    hourly_rate numeric(10,2) NOT NULL,
    CONSTRAINT listings_hourly_rate_check CHECK ((hourly_rate > (0)::numeric)),
    CONSTRAINT listings_max_guests_check CHECK ((max_guests > 0)),
    CONSTRAINT listings_sq_ft_check CHECK ((sq_ft > 0))
);


ALTER TABLE public.listings OWNER TO nathantjahjadi;

--
-- Name: listings_id_seq; Type: SEQUENCE; Schema: public; Owner: nathantjahjadi
--

CREATE SEQUENCE public.listings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.listings_id_seq OWNER TO nathantjahjadi;

--
-- Name: listings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nathantjahjadi
--

ALTER SEQUENCE public.listings_id_seq OWNED BY public.listings.id;


--
-- Name: messages; Type: TABLE; Schema: public; Owner: nathantjahjadi
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    sender_user_id integer NOT NULL,
    recipient_user_id integer NOT NULL,
    subject character varying(100) NOT NULL,
    message character varying(10000) NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.messages OWNER TO nathantjahjadi;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: nathantjahjadi
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_id_seq OWNER TO nathantjahjadi;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nathantjahjadi
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: reservations; Type: TABLE; Schema: public; Owner: nathantjahjadi
--

CREATE TABLE public.reservations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    listing_id integer NOT NULL,
    start_date date NOT NULL,
    start_time time without time zone NOT NULL,
    hours integer NOT NULL,
    guests integer NOT NULL,
    status character varying(30) NOT NULL,
    CONSTRAINT reservations_guests_check CHECK ((guests > 0)),
    CONSTRAINT reservations_hours_check CHECK ((hours > 0))
);


ALTER TABLE public.reservations OWNER TO nathantjahjadi;

--
-- Name: reservations_id_seq; Type: SEQUENCE; Schema: public; Owner: nathantjahjadi
--

CREATE SEQUENCE public.reservations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reservations_id_seq OWNER TO nathantjahjadi;

--
-- Name: reservations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nathantjahjadi
--

ALTER SEQUENCE public.reservations_id_seq OWNED BY public.reservations.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: nathantjahjadi
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    email character varying(50) NOT NULL,
    password character varying(100) NOT NULL
);


ALTER TABLE public.users OWNER TO nathantjahjadi;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: nathantjahjadi
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO nathantjahjadi;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nathantjahjadi
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Name: listings id; Type: DEFAULT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.listings ALTER COLUMN id SET DEFAULT nextval('public.listings_id_seq'::regclass);


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: reservations id; Type: DEFAULT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.reservations ALTER COLUMN id SET DEFAULT nextval('public.reservations_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: nathantjahjadi
--

COPY public.images (id, listing_id, original_filename, filename, url) FROM stdin;
8	3	backyard.png	67b0b3d3ae354c0bbb68c0cf5821c3ed.png	https://r33anotherbnb.s3.us-west-1.amazonaws.com/67b0b3d3ae354c0bbb68c0cf5821c3ed.png
9	3	backyard_side_angle1.png	4627e72086aa428eb0799bd7329b4400.png	https://r33anotherbnb.s3.us-west-1.amazonaws.com/4627e72086aa428eb0799bd7329b4400.png
10	3	backyard_side_angle2.png	ff44679fd97a4979a75325fd48c3534b.png	https://r33anotherbnb.s3.us-west-1.amazonaws.com/ff44679fd97a4979a75325fd48c3534b.png
11	3	backyard_hammock.png	d01d9fc6c4eb402db710b9c2ec5764ec.png	https://r33anotherbnb.s3.us-west-1.amazonaws.com/d01d9fc6c4eb402db710b9c2ec5764ec.png
12	3	shaded_seating.png	110a5bbb8fcd490cb5ed6ca268ec9f24.png	https://r33anotherbnb.s3.us-west-1.amazonaws.com/110a5bbb8fcd490cb5ed6ca268ec9f24.png
13	3	shaded_seating_side_angle.webp	57fc2cac88b14471beff6f7862f0a573.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/57fc2cac88b14471beff6f7862f0a573.webp
14	4	sky_view.webp	218d9db3c74844ceb6cdc7bcbae48944.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/218d9db3c74844ceb6cdc7bcbae48944.webp
15	4	backyard.webp	32af9059b2a6405da6df7f681d997bed.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/32af9059b2a6405da6df7f681d997bed.webp
16	4	grill.webp	c9132119560e407ba0d94e6dcce3a3fd.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/c9132119560e407ba0d94e6dcce3a3fd.webp
17	4	shaded_seating.webp	17bf5bb722354ef7964b112134e044e5.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/17bf5bb722354ef7964b112134e044e5.webp
18	4	additional_shaded_seating.webp	ba891f06868d444ebcd2aa14a0876d51.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/ba891f06868d444ebcd2aa14a0876d51.webp
19	4	lake_view.webp	5384321ac2ab4a689b2da632b68c1799.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/5384321ac2ab4a689b2da632b68c1799.webp
20	4	hammock_floor.webp	4dd25e005ac44ef097a69df1407aa417.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/4dd25e005ac44ef097a69df1407aa417.webp
21	5	pool.webp	6e673174ae9a4f4193409513919d701d.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/6e673174ae9a4f4193409513919d701d.webp
22	5	pool_angle_2.webp	9cb05fe7c25045f69e0815a69200eead.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/9cb05fe7c25045f69e0815a69200eead.webp
23	5	seating.webp	978ee1725d904115b6dc7f7e3fac7f27.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/978ee1725d904115b6dc7f7e3fac7f27.webp
24	5	cabana.webp	c4eb2a50a31246df90637bf3200e5a82.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/c4eb2a50a31246df90637bf3200e5a82.webp
25	5	fireplace.jpg	28ae41b6885a477998bc74f1a28d13ff.jpg	https://r33anotherbnb.s3.us-west-1.amazonaws.com/28ae41b6885a477998bc74f1a28d13ff.jpg
26	5	fireplace_2.webp	3b3bdb6ec8fc4ee0bc3ad58b88a5bec5.webp	https://r33anotherbnb.s3.us-west-1.amazonaws.com/3b3bdb6ec8fc4ee0bc3ad58b88a5bec5.webp
\.


--
-- Data for Name: listings; Type: TABLE DATA; Schema: public; Owner: nathantjahjadi
--

COPY public.listings (id, user_id, title, description, sq_ft, max_guests, hourly_rate) FROM stdin;
3	1	Charming backyard	Amenities: shaded seating, grill, hammock, cornhole	1000	15	45.00
4	4	Waterfront estate backyard	New deck installed with ample shaded seating, access to grill, and hammock floor above the water	1200	20	85.00
5	3	Pool next to golf course	Private backyard pool with fireplace, cabana, and grill.	660	18	67.00
\.


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: nathantjahjadi
--

COPY public.messages (id, sender_user_id, recipient_user_id, subject, message, "timestamp") FROM stdin;
1	2	1	Charming backyard	Do y'all allow dogs?	2023-10-13 17:13:16.558732
2	2	4	Waterfront estate backyard	Do you provide life jackets/vests?	2023-10-13 17:13:16.558732
3	2	3	Pool next to golf course	Do we need to bring our own firewood?	2023-10-13 17:13:16.558732
4	5	1	Charming backyard	How many cars can park there? 	2023-10-13 17:13:16.558732
\.


--
-- Data for Name: reservations; Type: TABLE DATA; Schema: public; Owner: nathantjahjadi
--

COPY public.reservations (id, user_id, listing_id, start_date, start_time, hours, guests, status) FROM stdin;
1	2	3	2023-10-27	18:30:00	6	8	requested
2	2	5	2023-11-25	14:15:00	8	18	requested
3	2	4	2024-02-17	12:00:00	12	19	requested
4	5	3	2023-10-18	18:30:00	4	4	requested
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: nathantjahjadi
--

COPY public.users (id, username, email, password) FROM stdin;
1	nate	nate@gmail.com	$2b$12$xvQQ7yB80xcM.KRelFdL8ulKh4SgHj3jCW4R.wcRo6WFot2tjRYzS
2	henry	henry@gmail.com	$2b$12$Ew/KEj9b7iJFoZNPCSm3Me5aeLoHETf5lliN4pBKDs3L8IHwqRecK
3	tuckerdiane	tuckerdiane@gmail.com	$2b$12$vr/8PaQsSXuU9GKu6ReCEOhShVBEY4ncRE1vM6J7WKtrlilKfZYde
4	mary	mary@gmail.com	$2b$12$3cDdODOAKyzp.uzlWxtrLuFsdAiML.j3fgHrEr/kNDe40eiRskTi.
5	lily	lily@gmail.com	$2b$12$JIpcN9X1ASQ8eh0wZn6unu74epnrdRIUNt3vyurh5meDcBFMQXxR6
\.


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nathantjahjadi
--

SELECT pg_catalog.setval('public.images_id_seq', 26, true);


--
-- Name: listings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nathantjahjadi
--

SELECT pg_catalog.setval('public.listings_id_seq', 5, true);


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nathantjahjadi
--

SELECT pg_catalog.setval('public.messages_id_seq', 4, true);


--
-- Name: reservations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nathantjahjadi
--

SELECT pg_catalog.setval('public.reservations_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nathantjahjadi
--

SELECT pg_catalog.setval('public.users_id_seq', 5, true);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: listings listings_pkey; Type: CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.listings
    ADD CONSTRAINT listings_pkey PRIMARY KEY (id);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: images images_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE;


--
-- Name: listings listings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.listings
    ADD CONSTRAINT listings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_recipient_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_recipient_user_id_fkey FOREIGN KEY (recipient_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: messages messages_sender_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_sender_user_id_fkey FOREIGN KEY (sender_user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: reservations reservations_listing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_listing_id_fkey FOREIGN KEY (listing_id) REFERENCES public.listings(id) ON DELETE CASCADE;


--
-- Name: reservations reservations_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: nathantjahjadi
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

