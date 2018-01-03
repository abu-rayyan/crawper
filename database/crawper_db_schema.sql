--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

-- Started on 2018-01-03 10:50:16

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
-- TOC entry 2901 (class 0 OID 0)
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
-- TOC entry 2902 (class 0 OID 0)
-- Dependencies: 217
-- Name: TABLE categories; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE categories IS 'Contains Ctaegories addresses included:
1. New Releases (Sports & Outdoors, Toys, Game & Baby)
2. Best Sellers ( Sports & Outdoors, Toys, Games & Baby)
3. Beauty & Health Care (Last 90 days)';


--
-- TOC entry 223 (class 1259 OID 33229)
-- Name: product_triggers; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE product_triggers (
    product_asin character varying(48) NOT NULL,
    overlapped_reviews boolean NOT NULL,
    vw_comparison boolean NOT NULL,
    one_off_reviewers boolean NOT NULL,
    abnormal_reviewer_participation boolean NOT NULL,
    multiple_single_day_reviews boolean NOT NULL,
    repeated_remarks boolean NOT NULL,
    review_spikes boolean NOT NULL,
    rating_trend boolean NOT NULL,
    three_stars_ratio boolean NOT NULL,
    total_triggers integer NOT NULL
);


ALTER TABLE product_triggers OWNER TO postgres;

--
-- TOC entry 2903 (class 0 OID 0)
-- Dependencies: 223
-- Name: TABLE product_triggers; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE product_triggers IS 'contains analyzed triggers about product data';


--
-- TOC entry 2904 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.product_asin; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.product_asin IS 'asin number of the product';


--
-- TOC entry 2905 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.overlapped_reviews; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.overlapped_reviews IS 'Trigger is activated if the same reviewers of a product were also the reviewers of 10 or more other products that they also gave 4-5 stars';


--
-- TOC entry 2906 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.vw_comparison; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.vw_comparison IS 'Trigger is activated if the length of a 4-5 star review is less than 25% or more than double the length of the average review of the product';


--
-- TOC entry 2907 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.one_off_reviewers; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.one_off_reviewers IS 'Trigger is activated for reviewers giving only 1 review that is also a 4-5 star review';


--
-- TOC entry 2908 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.abnormal_reviewer_participation; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.abnormal_reviewer_participation IS 'Trigger is activated if the concentration of 4-5 star ratings is more than what we’d expect to see from a reviewer for any category based on their participation history from column R';


--
-- TOC entry 2909 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.multiple_single_day_reviews; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.multiple_single_day_reviews IS 'Trigger is activated if there are more than 3 same-day 4-5 star reviews from the same reviewer';


--
-- TOC entry 2910 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.repeated_remarks; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.repeated_remarks IS 'Trigger is activated for a 4-5 star review if there is a phrase repeat in that review and the product being reviewed also has same phrase repeats in more than 20% of its total reviews';


--
-- TOC entry 2911 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.review_spikes; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.review_spikes IS 'Trigger is activated if number of the number of reviews on any day is more than 2 times the average review frequency for that product';


--
-- TOC entry 2912 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.rating_trend; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.rating_trend IS 'Trigger is activated if the first 5% of the ratings a product received were (1-2 stars) were followed by a sudden increase of (4-5 stars) ratings of more than 80% of the total number of initial (1-2 star) ratings the product received';


--
-- TOC entry 2913 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.three_stars_ratio; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.three_stars_ratio IS 'Trigger is activated if trigger "rating_trend" is activated and the percentage of 3 star ratings for a product is less than 20% of the total 1-2 star ratings';


--
-- TOC entry 2914 (class 0 OID 0)
-- Dependencies: 223
-- Name: COLUMN product_triggers.total_triggers; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN product_triggers.total_triggers IS 'Sum of triggers: Here, Abnormal Reviewer Category Participation- (Trigger #4) is given 0.5 weight and the remaining 9 triggers are given a weight of 1 each';


--
-- TOC entry 218 (class 1259 OID 16613)
-- Name: products; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE products (
    product_asin character varying NOT NULL,
    product_title text NOT NULL,
    product_price character varying NOT NULL,
    reviews_link text NOT NULL,
    category_name character varying NOT NULL,
    product_link text NOT NULL,
    total_reviews character varying NOT NULL
);


ALTER TABLE products OWNER TO postgres;

--
-- TOC entry 2915 (class 0 OID 0)
-- Dependencies: 218
-- Name: TABLE products; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE products IS 'Contain information of products from all categories in categories table';


--
-- TOC entry 222 (class 1259 OID 33216)
-- Name: products_analysis; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE products_analysis (
    product_asin character varying(48) NOT NULL,
    repeated_remarks text NOT NULL,
    repeated_phrase_frequency integer NOT NULL,
    percent_reviews_with_common_phrase real NOT NULL,
    reviewer_frequency integer NOT NULL,
    reviewer_participation character varying(4) NOT NULL,
    product_score integer NOT NULL
);


ALTER TABLE products_analysis OWNER TO postgres;

--
-- TOC entry 2916 (class 0 OID 0)
-- Dependencies: 222
-- Name: TABLE products_analysis; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE products_analysis IS 'Contains analysis data related to a particular product';


--
-- TOC entry 2917 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.product_asin; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.product_asin IS 'Unique asin muber of the product';


--
-- TOC entry 2918 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.repeated_remarks; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.repeated_remarks IS 'Most commonly repeated phrases of length 3 (common to reviews for same products). ';


--
-- TOC entry 2919 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.repeated_phrase_frequency; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.repeated_phrase_frequency IS 'Number of a product’s reviews in which most common phrase occurred.';


--
-- TOC entry 2920 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.percent_reviews_with_common_phrase; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.percent_reviews_with_common_phrase IS 'Percentage of a product’s reviews that used the most commonly occurring phrase';


--
-- TOC entry 2921 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.reviewer_frequency; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.reviewer_frequency IS 'Number of times a reviewer has given review';


--
-- TOC entry 2922 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.reviewer_participation; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.reviewer_participation IS 'Depending on how many times a reviewer has given review, a label value will be assigned:
0- 1: ''R1''
2-5: ''R2''
6- 10: ''R3''
11-20: ''R4''
21- 30: ''R5''
31- 40: ''R6''

Column Q- Reviewer Frequency
Number of times a reviewer has given review
Column R- Reviewer Participation History
Depending on how many times a reviewer has given review, a label value will be assigned:
0- 1: ''R1''
2-5: ''R2''
6- 10: ''R3''
11-20: ''R4''
21- 30: ''R5''
31- 40: ''R6''
41- 50: ''R7''
51- 60: ''R8''
61 onwards: ''R9''
';


--
-- TOC entry 2923 (class 0 OID 0)
-- Dependencies: 222
-- Name: COLUMN products_analysis.product_score; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN products_analysis.product_score IS 'Represents the overall product score which is determined by:
. The number of reviews a product has received.
. The individual review scores of all the reviews a product has received
';


--
-- TOC entry 220 (class 1259 OID 16660)
-- Name: reviewers; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE reviewers (
    reviewer_id character varying(48) NOT NULL,
    reviewer_name character varying(24) NOT NULL,
    profile_link text NOT NULL,
    total_reviews integer NOT NULL,
    creduality_score real NOT NULL
);


ALTER TABLE reviewers OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16626)
-- Name: reviews; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE reviews (
    review_link text NOT NULL,
    product_asin character varying(24) NOT NULL,
    review_title text NOT NULL,
    review_text text NOT NULL,
    review_rate character varying NOT NULL,
    reviewer_id character varying(48) NOT NULL,
    review_date character varying NOT NULL
);


ALTER TABLE reviews OWNER TO postgres;

--
-- TOC entry 2924 (class 0 OID 0)
-- Dependencies: 219
-- Name: TABLE reviews; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE reviews IS 'Contain information about reviews of a product';


--
-- TOC entry 221 (class 1259 OID 33115)
-- Name: reviews_analysis; Type: TABLE; Schema: crawper; Owner: postgres
--

CREATE TABLE reviews_analysis (
    review_link text NOT NULL,
    review_length integer NOT NULL,
    word_count_category character varying NOT NULL,
    sentiment_score real NOT NULL,
    sentiment_label character varying NOT NULL,
    common_phrase boolean NOT NULL,
    credulity_score real NOT NULL,
    review_scores integer NOT NULL
);


ALTER TABLE reviews_analysis OWNER TO postgres;

--
-- TOC entry 2925 (class 0 OID 0)
-- Dependencies: 221
-- Name: TABLE reviews_analysis; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON TABLE reviews_analysis IS 'Contains analysis of reviews of a product';


--
-- TOC entry 2926 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.review_link; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.review_link IS 'link of the review as pkey and fkey';


--
-- TOC entry 2927 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.review_length; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.review_length IS 'total length of the review text';


--
-- TOC entry 2928 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.word_count_category; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.word_count_category IS 'B: If review length is close to average review length of the product
A: if review length is less than 25% of average review length of the product (as found by 50% randomly picked samples)
C: if review length is more than double of average review length of the product (as found by 50% randomly picked samples)
';


--
-- TOC entry 2929 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.sentiment_score; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.sentiment_score IS 'Its range is -100 to +100. It represents sentiment of a review text.
Closer this value is to 100, more positive the emotion is.
Closer this value is to -100, more negative the emotion is.
';


--
-- TOC entry 2930 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.sentiment_label; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.sentiment_label IS 'if -100<= score <-50:
sentiment= ''angry''
if -50<= score <-10:
sentiment= ''dissatisfied''
if -10<= score <10:
sentiment= ''neutral''
if 10<= score <50:
sentiment= ''satisfied''
if 50<= score <=100:
sentiment= ''happy''
';


--
-- TOC entry 2931 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.common_phrase; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.common_phrase IS 'Is most common phrase (common to the review itself) present?
True if yes, False if no
';


--
-- TOC entry 2932 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.credulity_score; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.credulity_score IS 'Higher this value is, more easily that person is pleased and hence lesser the weightage of his review';


--
-- TOC entry 2933 (class 0 OID 0)
-- Dependencies: 221
-- Name: COLUMN reviews_analysis.review_scores; Type: COMMENT; Schema: crawper; Owner: postgres
--

COMMENT ON COLUMN reviews_analysis.review_scores IS 'These scores represent the cumulative combined effect of RATING, REVIEW SENTIMENTS & CREDULITY scores. 
A factor of 60 is added to the GREEN (can be adjusted in line 526).
A factor of 30 is added to the YELLOW score (can be adjusted in line 528).
RED Review score = -60 (can be adjusted in line 522)
';


--
-- TOC entry 2758 (class 2606 OID 24594)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_name);


--
-- TOC entry 2770 (class 2606 OID 33233)
-- Name: product_triggers product_triggers_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY product_triggers
    ADD CONSTRAINT product_triggers_pkey PRIMARY KEY (product_asin);


--
-- TOC entry 2768 (class 2606 OID 33223)
-- Name: products_analysis products_analysis_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY products_analysis
    ADD CONSTRAINT products_analysis_pkey PRIMARY KEY (product_asin);


--
-- TOC entry 2760 (class 2606 OID 24605)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_asin);


--
-- TOC entry 2764 (class 2606 OID 16664)
-- Name: reviewers reviewer_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviewers
    ADD CONSTRAINT reviewer_pkey PRIMARY KEY (reviewer_id);


--
-- TOC entry 2766 (class 2606 OID 33207)
-- Name: reviews_analysis reviews_analysis_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews_analysis
    ADD CONSTRAINT reviews_analysis_pkey PRIMARY KEY (review_link);


--
-- TOC entry 2762 (class 2606 OID 16633)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_link);


--
-- TOC entry 2775 (class 2606 OID 33234)
-- Name: product_triggers product_trigger's fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY product_triggers
    ADD CONSTRAINT "product_trigger's fkey" FOREIGN KEY (product_asin) REFERENCES products(product_asin);


--
-- TOC entry 2774 (class 2606 OID 33224)
-- Name: products_analysis products_analysis_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY products_analysis
    ADD CONSTRAINT products_analysis_fkey FOREIGN KEY (product_asin) REFERENCES products(product_asin);


--
-- TOC entry 2771 (class 2606 OID 24595)
-- Name: products products_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY products
    ADD CONSTRAINT products_fkey FOREIGN KEY (category_name) REFERENCES categories(category_name);


--
-- TOC entry 2773 (class 2606 OID 33208)
-- Name: reviews_analysis reviews_analysis_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews_analysis
    ADD CONSTRAINT reviews_analysis_fkey FOREIGN KEY (review_link) REFERENCES reviews(review_link);


--
-- TOC entry 2772 (class 2606 OID 24606)
-- Name: reviews reviews_fkey; Type: FK CONSTRAINT; Schema: crawper; Owner: postgres
--

ALTER TABLE ONLY reviews
    ADD CONSTRAINT reviews_fkey FOREIGN KEY (product_asin) REFERENCES products(product_asin);


-- Completed on 2018-01-03 10:50:16

--
-- PostgreSQL database dump complete
--

