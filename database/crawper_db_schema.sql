--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

-- Started on 2017-12-29 12:15:15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 7 (class 2615 OID 16604)
-- Name: crawper; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA crawper;


ALTER SCHEMA crawper OWNER TO postgres;

--
-- TOC entry 2881 (class 0 OID 0)
-- Dependencies: 7
-- Name: SCHEMA crawper; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA crawper IS 'contains crawled and scraped data of crawper';


SET search_path = crawper, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 217 (class 1259 OID 16605)
-- Name: categories; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE categories (
    category_name character varying NOT NULL
);


ALTER TABLE categories OWNER TO postgres;

--
-- TOC entry 2882 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE categories; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE categories IS 'Contains Ctaegories addresses included:
1. New Releases (Sports & Outdoors, Toys, Game & Baby)
2. Best Sellers ( Sports & Outdoors, Toys, Games & Baby)
3. Beauty & Health Care (Last 90 days)';


--
-- TOC entry 218 (class 1259 OID 16613)
-- Name: products; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE products (
    product_asin character varying NOT NULL,
    product_title text NOT NULL,
    product_price character varying,
    reviews_link text,
    category_name character varying NOT NULL,
    product_link text NOT NULL,
    total_reviews character varying
);


ALTER TABLE products OWNER TO postgres;

--
-- TOC entry 2883 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE products; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE products IS 'Contain information of products from all categories in categories table';


--
-- TOC entry 220 (class 1259 OID 16660)
-- Name: reviewers; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE reviewers (
    reviewer_id character varying(48) NOT NULL,
    reviewer_name character varying(24) NOT NULL,
    profile_link text NOT NULL
);


ALTER TABLE reviewers OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16626)
-- Name: reviews; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE reviews (
    review_link text NOT NULL,
    product_asin character varying(24) NOT NULL,
    review_title text,
    review_text text,
    review_rate character varying(12),
    reviewer_id character varying(48) NOT NULL,
    review_date character varying(24)
);


ALTER TABLE reviews OWNER TO postgres;

--
-- TOC entry 2884 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE reviews; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE reviews IS 'Contain information about reviews of a product';


--
-- TOC entry 2744 (class 2606 OID 24594)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_name);


--
-- TOC entry 2746 (class 2606 OID 24605)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_asin);


--
-- TOC entry 2748 (class 2606 OID 16666)
-- Name: reviews reviewer_id_con; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviewer_id_con UNIQUE (reviewer_id);


--
-- TOC entry 2752 (class 2606 OID 16664)
-- Name: reviewers reviewer_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviewers
    ADD CONSTRAINT reviewer_pkey PRIMARY KEY (reviewer_id);


--
-- TOC entry 2750 (class 2606 OID 16633)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_link);


--
-- TOC entry 2753 (class 2606 OID 24595)
-- Name: products products_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY products
    ADD CONSTRAINT products_fkey FOREIGN KEY (category_name) REFERENCES categories(category_name);


--
-- TOC entry 2755 (class 2606 OID 16667)
-- Name: reviewers reviewers_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviewers
    ADD CONSTRAINT reviewers_fkey FOREIGN KEY (reviewer_id) REFERENCES reviews(reviewer_id);


--
-- TOC entry 2754 (class 2606 OID 24606)
-- Name: reviews reviews_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_fkey FOREIGN KEY (product_asin) REFERENCES products(product_asin);


-- Completed on 2017-12-29 12:15:15

--
-- PostgreSQL database dump complete
--

