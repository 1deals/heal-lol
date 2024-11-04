--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)
-- Dumped by pg_dump version 16.4 (Ubuntu 16.4-0ubuntu0.24.04.2)

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

--
-- Name: voicemaster; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA voicemaster;


ALTER SCHEMA voicemaster OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: afk; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.afk (
    user_id bigint NOT NULL,
    status text,
    "time" bigint
);


ALTER TABLE public.afk OWNER TO postgres;

--
-- Name: api_key; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.api_key (
    id integer NOT NULL,
    key text NOT NULL,
    user_id bigint NOT NULL,
    role text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.api_key OWNER TO postgres;

--
-- Name: api_key_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.api_key_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_key_id_seq OWNER TO postgres;

--
-- Name: api_key_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.api_key_id_seq OWNED BY public.api_key.id;


--
-- Name: authed; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authed (
    guild_id bigint NOT NULL
);


ALTER TABLE public.authed OWNER TO postgres;

--
-- Name: autoresponder; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autoresponder (
    guild_id bigint NOT NULL,
    trigger text NOT NULL,
    response text,
    id text,
    strict boolean DEFAULT true
);


ALTER TABLE public.autoresponder OWNER TO postgres;

--
-- Name: autorole; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autorole (
    guild_id bigint NOT NULL,
    role_id bigint
);


ALTER TABLE public.autorole OWNER TO postgres;

--
-- Name: blacklist; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blacklist (
    user_id bigint NOT NULL
);


ALTER TABLE public.blacklist OWNER TO postgres;

--
-- Name: blacklistguild; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blacklistguild (
    guild_id bigint NOT NULL
);


ALTER TABLE public.blacklistguild OWNER TO postgres;

--
-- Name: booster_module; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booster_module (
    guild_id bigint NOT NULL,
    base bigint NOT NULL
);


ALTER TABLE public.booster_module OWNER TO postgres;

--
-- Name: booster_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.booster_roles (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.booster_roles OWNER TO postgres;

--
-- Name: boostmessage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.boostmessage (
    guild_id bigint NOT NULL,
    message text,
    channel_id bigint
);


ALTER TABLE public.boostmessage OWNER TO postgres;

--
-- Name: br_award; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.br_award (
    guild_id bigint NOT NULL,
    role_id bigint NOT NULL
);


ALTER TABLE public.br_award OWNER TO postgres;

--
-- Name: cases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cases (
    guild_id bigint NOT NULL,
    count bigint
);


ALTER TABLE public.cases OWNER TO postgres;

--
-- Name: chatbot; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.chatbot (
    guild_id bigint NOT NULL,
    channel_id bigint
);


ALTER TABLE public.chatbot OWNER TO postgres;

--
-- Name: counters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.counters (
    guild_id bigint NOT NULL,
    channel_type text,
    channel_id bigint,
    channel_name text,
    module text
);


ALTER TABLE public.counters OWNER TO postgres;

--
-- Name: disablecommand; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.disablecommand (
    guild_id bigint NOT NULL,
    command text NOT NULL
);


ALTER TABLE public.disablecommand OWNER TO postgres;

--
-- Name: economy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.economy (
    user_id bigint NOT NULL,
    cash bigint,
    bank bigint
);


ALTER TABLE public.economy OWNER TO postgres;

--
-- Name: filter; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.filter (
    guild_id bigint NOT NULL,
    mode text NOT NULL,
    rule_id bigint NOT NULL
);


ALTER TABLE public.filter OWNER TO postgres;

--
-- Name: forcenick; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.forcenick (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    name text
);


ALTER TABLE public.forcenick OWNER TO postgres;

--
-- Name: globalban; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.globalban (
    user_id bigint
);


ALTER TABLE public.globalban OWNER TO postgres;

--
-- Name: guild_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.guild_settings (
    guild_id bigint NOT NULL,
    leveling_enabled boolean DEFAULT false NOT NULL
);


ALTER TABLE public.guild_settings OWNER TO postgres;

--
-- Name: guilds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.guilds (
    guild_id bigint NOT NULL,
    prefix character varying(5)
);


ALTER TABLE public.guilds OWNER TO postgres;

--
-- Name: invoke; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.invoke (
    guild_id bigint NOT NULL,
    type text NOT NULL,
    message text
);


ALTER TABLE public.invoke OWNER TO postgres;

--
-- Name: joindm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.joindm (
    guild_id bigint NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.joindm OWNER TO postgres;

--
-- Name: joinping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.joinping (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.joinping OWNER TO postgres;

--
-- Name: lastfm; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lastfm (
    user_id bigint NOT NULL,
    lfuser text,
    mode text,
    command text
);


ALTER TABLE public.lastfm OWNER TO postgres;

--
-- Name: levels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.levels (
    user_id bigint NOT NULL,
    message_count integer DEFAULT 0 NOT NULL,
    level integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.levels OWNER TO postgres;

--
-- Name: logging; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logging (
    guild_id bigint NOT NULL,
    joinlogschannel bigint,
    leavelogschannel bigint,
    messagelogschannel bigint,
    voicelogschannel bigint
);


ALTER TABLE public.logging OWNER TO postgres;

--
-- Name: modlogs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.modlogs (
    guild_id bigint NOT NULL,
    channel_id bigint
);


ALTER TABLE public.modlogs OWNER TO postgres;

--
-- Name: names; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.names (
    user_id bigint NOT NULL,
    oldnames text,
    "time" integer
);


ALTER TABLE public.names OWNER TO postgres;

--
-- Name: premium; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.premium (
    user_id bigint NOT NULL
);


ALTER TABLE public.premium OWNER TO postgres;

--
-- Name: restore; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restore (
    guild_id bigint NOT NULL,
    user_id bigint NOT NULL,
    role bigint
);


ALTER TABLE public.restore OWNER TO postgres;

--
-- Name: restricted_words; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.restricted_words (
    guild_id bigint NOT NULL,
    word text NOT NULL
);


ALTER TABLE public.restricted_words OWNER TO postgres;

--
-- Name: selfprefix; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.selfprefix (
    user_id bigint NOT NULL,
    prefix text
);


ALTER TABLE public.selfprefix OWNER TO postgres;

--
-- Name: starboard; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.starboard (
    guild_id bigint NOT NULL,
    channel_id bigint,
    emoji text,
    threshold bigint
);


ALTER TABLE public.starboard OWNER TO postgres;

--
-- Name: timezones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.timezones (
    user_id bigint NOT NULL,
    timezone text
);


ALTER TABLE public.timezones OWNER TO postgres;

--
-- Name: topcmds; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.topcmds (
    command_name text NOT NULL,
    usage_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.topcmds OWNER TO postgres;

--
-- Name: usage; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usage (
    amount bigint DEFAULT 0 NOT NULL
);


ALTER TABLE public.usage OWNER TO postgres;

--
-- Name: usertracker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usertracker (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.usertracker OWNER TO postgres;

--
-- Name: uwulock; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.uwulock (
    guild_id bigint,
    user_id bigint
);


ALTER TABLE public.uwulock OWNER TO postgres;

--
-- Name: vanityroles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vanityroles (
    guild_id bigint NOT NULL,
    channel_id bigint,
    text text,
    role_id bigint
);


ALTER TABLE public.vanityroles OWNER TO postgres;

--
-- Name: vanitytracker; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vanitytracker (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE public.vanitytracker OWNER TO postgres;

--
-- Name: vape; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vape (
    user_id bigint NOT NULL,
    flavor text,
    hits bigint
);


ALTER TABLE public.vape OWNER TO postgres;

--
-- Name: vc_stats; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vc_stats (
    user_id bigint NOT NULL,
    total_time bigint DEFAULT 0
);


ALTER TABLE public.vc_stats OWNER TO postgres;

--
-- Name: welcome; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.welcome (
    guild_id bigint NOT NULL,
    channel_id bigint,
    message text
);


ALTER TABLE public.welcome OWNER TO postgres;

--
-- Name: channels; Type: TABLE; Schema: voicemaster; Owner: postgres
--

CREATE TABLE voicemaster.channels (
    guild_id bigint NOT NULL,
    owner_id bigint NOT NULL,
    channel_id bigint NOT NULL
);


ALTER TABLE voicemaster.channels OWNER TO postgres;

--
-- Name: configuration; Type: TABLE; Schema: voicemaster; Owner: postgres
--

CREATE TABLE voicemaster.configuration (
    guild_id bigint NOT NULL,
    channel_id bigint NOT NULL,
    interface_id bigint NOT NULL,
    category_id bigint NOT NULL
);


ALTER TABLE voicemaster.configuration OWNER TO postgres;

--
-- Name: api_key id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_key ALTER COLUMN id SET DEFAULT nextval('public.api_key_id_seq'::regclass);


--
-- Data for Name: afk; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.afk (user_id, status, "time") FROM stdin;
878363386918862888	shower	1725252044
1169780415385587762	sleeping like a dog ^-^	1725328678
549804055275372544	sleeping	1725334524
954563508576595968	snoring <:zzz:983499584380755968>	1725334654
\.


--
-- Data for Name: api_key; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.api_key (id, key, user_id, role, created_at) FROM stdin;
1	6kmq9NIaehkAx7R4o7I5xxSIpIatKEKVMt9NjHyjl6c	187747524646404105	master	2024-08-23 16:07:43.108346
2	iKYdXRJ0Hzv-_5GREYyJuO4879K4VRlna9NM-gNt_4I	971464344749629512	master	2024-08-31 18:22:14.206921
3	aeKbW25tNaOYeots20tDpYaY6itqhCAafTn5BSXRZaw	394152799799345152	master	2024-08-31 20:57:33.630611
4	TMN6aVmzO2gjomeJIATaGhZAQEvsNcx2G0DAJxB61Uk	1234025578232025122	master	2024-09-03 13:57:59.273458
5	w21MgGA9WY4iVjlXMqUngqI8We9_Gs4euxTLG2RutmM	1233417695974789172	master	2024-09-26 10:06:16.522077
\.


--
-- Data for Name: authed; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authed (guild_id) FROM stdin;
1268614947018113084
1279205866993877085
1281680936316178482
1277320283119943760
1281980873041772685
1281833006943961139
1282393410204078141
1282466911870783518
1282563196120727663
1279344689165635604
\.


--
-- Data for Name: autoresponder; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autoresponder (guild_id, trigger, response, id, strict) FROM stdin;
1244403114447212564	hiya	bye	TxFJBnYiTz	t
1244403114447212564	variables	{embed}$v{description: Variables can be found here }$v{button: label: variables && url: https://heal-2.gitbook.io/docs }$v{content: {user.mention}}	GeENEKUCcf	t
1270486377460404356	<@1160907025434279976>	don’t kno you	VpnrBmEZXg	t
1244403114447212564	vote	{embed}$v{description: Enjoy using the bot? [Vote here!](https://top.gg/bot/1232778508426809365/vote) }$v{button: label: vote me! && url: https://top.gg/bot/1232778508426809365/vote }	cGHNODzNVq	t
1272292232250265731	hello	test	qAyFqSDEpn	t
1260459692426006550	pic perms	rep /affair in status or boost server.	edVGSxdAXq	t
1260459692426006550	nigger	you got 2 more times mf	iHXcgJqaSy	t
1276605260110237758	pic perms	boost or rep /yuko for pic perms	DCfyOzCJsh	t
1244403114447212564	autoresponder	do `<prefix>ar add <trigger>, <response>`	zcwxSxKNab	t
1260459692426006550	picperms	boost or rep /affair in status	pDDRqtImTZ	t
1267058530175684759	pic In order to get pic perms boost	or rep /joints in status!<a:ggokeggpreciosaggjoints:1267472389823004754>	gpQlOAOhgd	t
1275204588894683247	pic perm	rep /pilot in custom status for pic	hiTvZeElBD	t
1281680936316178482	pic perms	boost or rep /swore for pic perms	ccmWEdLVjX	t
1227007783602491423	[pic]	[rep /try in status or profile for pic]	bczYcvkHpF	t
949837695050469456	pic perms	rep or boost 4 pic perms	HzfaTpbjZq	f
1244403114447212564	donate	send any donations to **heal@psutil.tech** on paypal	FeMchqQPrc	t
1227007783602491423	guild	boost twice for guild and owner<a:boost:1267728182199713844> <:bleed:1227353994146480179>	yczMgWLmgS	t
1227007783602491423	how do i join guild	boost twice for guild and owner<a:boost:1267728182199713844> <:bleed:1227353994146480179>	RADcCIgeLd	t
1282563196120727663	what is this server	it's a support server	rDUduAGFci	t
1289741574552424518	hey	sup	NxmtVxfBrE	t
1244403114447212564	<@1083131355984044082>	<:xiosex2:1292877646224429096>	fXhCGKoJHJ	t
1292985929954365472	woo	that’s big dick woo!	NHPXtdeXYc	t
1292985929954365472	repent	<@1218811875320660039>	dYpQlJyfIE	t
1292985929954365472	tuvy	<@795099082661298246>	TieBVAcfmo	t
1292985929954365472	<@1218811875320660039>	yo	dfTHLowuvc	t
1292985929954365472	pic	rep /outside for pic perms	BBVBSkijkj	t
1292985929954365472	pic perms	rep /outside for pic perms	ZzxAAkcUOe	t
1294660772361666603	yo	wsp {user.mention}	tJniwvwKFP	t
1295649687453438033	pp	https://www.paypal.me/JessseKoytila	mvIvMnFsir	t
1295649687453438033	paypal	https://www.paypal.me/JessseKoytila	wINQLJvDtW	t
1224770474257678356	trinity	firest nigga of all biggest dono	QwlCLgJrng	t
1299477839103660052	invfiltercontent	(https?://)?(www.)?(discord.(gg|io|me|li)|discordapp.com/invite|discord.com/invite)/.+[a-z]	UOlGXkhsQs	t
1291961786852970558	pic	rep **/bounty** and you will receive pic perms.	puejUqLNcJ	t
1291961786852970558	gif	rep **/bounty** and you will receive gif perms.	HuHwWOrHnm	f
1291961786852970558	perms	dm <@1286072791325478988> for perms.	jiYyMXOaBO	t
1291961786852970558	rape	no rape jokes	IfNuyQWUHX	f
1291961786852970558	🤡	dork {user.mention}	MhBQjiitAq	f
1291961786852970558	zero	you mean the king? {user.mention}	VHuEeoXPsq	f
1291961786852970558	skid	show me a script 🤓{user.mention}	EXVMgsReUN	f
1291961786852970558	larp	random saying larp {user.mention}	ZdLwkGrLDq	f
1291961786852970558	ratio	{user.mention} got ratioed	rspfxhrROg	f
1291961786852970558	bounty	oat {user.mention}	zLNQarYEIz	f
1291961786852970558	dead	inv ur friends kid {user.mention}	WDNMVfHtAv	f
1291961786852970558	kid	my king kid  {user.mention}	QxbmUsutlX	f
1291961786852970558	nut	in me {user.mention}	qvdQTsAyFP	f
1291961786852970558	vc	{user.mention} -https://discord.com/channels/1291961786852970558/1300665144182833152 <#1300639753615708201>	VqEsfPkCqF	f
1291961786852970558	fuck	https://cdn.discordapp.com/attachments/1115307735299391580/1258147443304828980/copy_59F74813-01CF-45CE-842C-2778818E8D57.gif	AbAZuozkFL	f
1291961786852970558	764	https://cdn.discordapp.com/attachments/1294622337949241409/1297405683100029000/attachment.gif	DNyMERbHTP	f
1291961786852970558	xeno	||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| https://cdn.discordapp.com/attachments/1300639257416831048/1300932628320485386/v09044g40000cqjche7og65on8tme7og.mov?ex=6722a36c&is=672151ec&hm=4f4cb91297ad970d7b8ed03bf450725347bc1f8704a073ba9b90adef0c4f43a7&	qzHAQSdklz	t
1291961786852970558	regret	||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| https://cdn.discordapp.com/attachments/1300639257416831048/1300958126929084437/v09044g40000cqjche7og65on8tme7og.mov?ex=6722bb2c&is=672169ac&hm=c5ba11eb4c1de2cbee2647de4d1aadbd3fb0b9614528194b8a2f1b770030a2dd&	POkPHzRRiB	t
1291961786852970558	rin	||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| https://cdn.discordapp.com/attachments/1300639257416831048/1300958126929084437/v09044g40000cqjche7og65on8tme7og.mov?ex=6722bb2c&is=672169ac&hm=c5ba11eb4c1de2cbee2647de4d1aadbd3fb0b9614528194b8a2f1b770030a2dd&	oRPYqYDjaR	t
1289990098649088111	paypal	donate <@1262799073077891155> please 🙏🏻 https://www.paypal.me/midzesty	mPLePMGzYS	t
949837695050469456	<@1154065198538305686> your master	he owns u <a:B_bunny002:1013135188458479688>	CmZwzLTPAO	t
1291961786852970558	fazo	That Boy is a Monster <:SSTotenkopf:1300143800475189288> ||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​||||​|| https://cdn.discordapp.com/attachments/1242464037032165548/1249097892514496573/twittervid.com_aryanclassics_98db22.mp4?ex=67102210&is=670ed090&hm=2ed6fd7d0e1ec5da7cc75a7aad1fb9c61884d138798f0dc58a59563052161f31& <@1219020551247630377>	LOEyKZFysd	t
\.


--
-- Data for Name: autorole; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.autorole (guild_id, role_id) FROM stdin;
1244403114447212564	1254787640922996878
1271502845161508884	1274345166932676618
1212420500366557264	1213854849406345338
1279837686542368880	1279838672593883156
1276605260110237758	1276605260110237759
1257987786888318987	1270114004148293664
1281680936316178482	1281680936316178487
1279205866993877085	1280575811342307490
1120434472114999307	1279986983787040768
1281980873041772685	1282067382231367760
1276302538152611972	1282104303414153237
1275204588894683247	1275206651720237127
1274776424477364286	1274779588052127825
1256851790540832831	1256851790540832834
1282393410204078141	1282745992109756518
1284532619383672853	1284533225611333642
1237392684113723423	1251837535336927273
1284756954933362688	1284775815158169694
1285720473627525333	1285720703756402721
1285074886582206484	1285074886640926774
949837695050469456	949839057310064671
1288186497585123340	1288190821803364363
1288335344969711678	1288616851017957476
1285832779216719967	1285857294705233944
1286215830194884619	1289257971985023117
965727249108193280	1288015537900879926
1289741574552424518	1290173573465374782
1290472403763335220	1290818503540211722
1281274638567080018	1281748651840110632
1292422832504176660	1292823365576425512
1293699972172091523	1293710531705704549
1050030051921506336	1050030051921506341
1287533179166523432	1290527846451773481
1295105048161812540	1295108577668894891
1295531878563971134	1295532205015302156
1151241272326099056	1285060953683263520
1288959741820665960	1293987063271653447
1279472645661917347	1279493978848366754
1291976014540570624	1291987876543729744
1296283710118826084	1296306148655501416
1295649687453438033	1295717976502308907
1292430925141119037	1297629537970028716
1298398436638326836	1298398704256024657
1224770474257678356	1224770474257678357
1232760919113863279	1232760919206006846
1291961786852970558	1294110285136924754
1274569048205824153	1300962950911365130
1301221390388822038	1301222870944452649
1256068630987145298	1301288397016535082
1119311424473276416	1119334703661584546
1121045839012438027	1293883806440226880
1302091501479919779	1302096282231373885
1299880499644334200	1301080492086657024
1296674979714170921	1302498215957893130
\.


--
-- Data for Name: blacklist; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blacklist (user_id) FROM stdin;
1207108276517605411
1088859356302413874
852784127447269396
1018558379238637578
1221894671052312748
1085901325524553737
1141137889808359584
1170109139989561464
1165739627148234822
1112766792025251913
1106121476932898946
1269255506753617963
1207202923054895154
345462882902867969
1083861728380584038
1006606704017932298
742371639127441448
1082976686846509086
1204863605405651008
991413994709590056
348064191971590145
1163080789957812285
1210548908426526732
1286752191042031638
1091393895667081267
989701837282238486
1229830301388243075
1163395242075115520
961046117334777857
609245913310953492
458546741285748736
1247770987210997793
255841984470712330
1125516730068893807
1290698569937981512
1049618225882734593
1273316981705146485
1280746666567401485
1247282517288157347
850387045398478868
1152771520763015228
1253339405901500456
\.


--
-- Data for Name: blacklistguild; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.blacklistguild (guild_id) FROM stdin;
1275204588894683247
1281680936316178482
1289990098649088111
\.


--
-- Data for Name: booster_module; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booster_module (guild_id, base) FROM stdin;
1183029663149334579	1183029663149334579
1118862694980788276	1124299850012442645
1267058530175684759	1267145175872962683
1274454080286232617	1278068010246078627
1286744833280573481	1287759340857462887
1260827368625279159	1263517159301316723
1221529993318891520	1245117337904873484
1290472403763335220	1290473648880226355
1284579437152702587	1289824528188440629
1293622337597603932	1294362832325840948
1294870137903517737	1294870137903517737
1295105048161812540	1295105048161812540
1294660772361666603	1294660772361666603
1296538895030161448	1296538895030161448
1299011532465635430	1299143660729925744
949837695050469456	949894180082167859
\.


--
-- Data for Name: booster_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.booster_roles (guild_id, user_id, role_id) FROM stdin;
1118862694980788276	977438272013881355	1284329632820101266
1286744833280573481	1262799073077891155	1287780880512716911
1221529993318891520	908356374294048799	1288597385840169042
1221529993318891520	1015363074636656650	1288949448038416427
1221529993318891520	1237846575955447869	1290776219931115594
949837695050469456	1291027133334032479	1302667456573083741
\.


--
-- Data for Name: boostmessage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.boostmessage (guild_id, message, channel_id) FROM stdin;
1268584157639082086	{embed}$v{content: {user.mention}}$v{author: {guild.name} @ {guild.boost_count} && {guild.icon}}$v{description:\n <:blank:1263954634037530685>\n [ty for boosting dm owner for custom role](https://discord.com/channels/1268584157639082086/1274043867586498634)}$v{color: #000000}$v{thumbnail: {user.avatar}}	1270696859865972738
1212420500366557264	appreciate you	1213854673216344124
1276605260110237758	thx for boosting /yuko {user.mention} , stay active	1276605260353245308
1281680936316178482	thx for boosting /yuko {user.mention} , stay active	1281680936337018939
1276302538152611972	{user.mention} ',br create' to make ur custom role	\N
1279205866993877085	\N	1279205866993877088
1284863818073112616	Thanks for boosting make a <#1284964289987219668> to get your award	\N
1260827368625279159	{user} ***thx for boosting pookie***	\N
1290472403763335220	**thx for boosting cutie {user.mention}**	1290818668183425115
1244403114447212564	{user.mention} thanks for boosting! We now have {guild.boost_count} boosts! <a:aliendance:1263984951066366155>	1293964677109518478
1294870137903517737	thx for boosting <:steambored:1265785956930420836>	1294885384634761218
1295531878563971134	tysm for boosting {user.mention} <:yeaa:1295554372834689064>	1295532276771192862
1295649687453438033	tysm for boosting {user.mention} <a:boosting:1295730588552003595>	1295714676344094780
1121045839012438027	\N	1293955892877987880
1280214704626728990	{content: {user.mention} ty for boosting, open a ticket in <#1299001456233549907> to claim your **booster role**.}	1299002450149249024
949837695050469456	{embed}$v{description: Thanks so much {user.mention} for boosting {guild.name}\n,br create <name>\n,br color <hex code\n,br icon <emoji>\n,br name <name>}$v{content: {user.mention}}$v{thumbnail: {user.avatar}}	1287449583240220712
1302091501479919779	\N	1302096317681766511
\.


--
-- Data for Name: br_award; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.br_award (guild_id, role_id) FROM stdin;
\.


--
-- Data for Name: cases; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cases (guild_id, count) FROM stdin;
1281274638567080018	1
1292985929954365472	306
1294870137903517737	11
1183029663149334579	4
1297293375204229120	4
1151241272326099056	60
1289787801973428288	1
949837695050469456	103
1244403114447212564	163
\.


--
-- Data for Name: chatbot; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.chatbot (guild_id, channel_id) FROM stdin;
1294660772361666603	1294661339850997760
1121045839012438027	1293955898909397113
1298398436638326836	1298438365615489064
1274164559296335922	1277447301664866315
\.


--
-- Data for Name: counters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.counters (guild_id, channel_type, channel_id, channel_name, module) FROM stdin;
\.


--
-- Data for Name: disablecommand; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.disablecommand (guild_id, command) FROM stdin;
1181509738459037768	icon
1181509738459037768	howlesbian
1289315449212764262	chatgpt
1289315449212764262	server
1289315449212764262	instagram
1292522369868365904	google
1292522369868365904	image
1289315449212764262	tiktok
1292522369868365904	reposter
1274164559296335922	ban
1274164559296335922	kick
1274164559296335922	create
1274164559296335922	rename
1274164559296335922	delete
1274164559296335922	nuke
\.


--
-- Data for Name: economy; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.economy (user_id, cash, bank) FROM stdin;
\.


--
-- Data for Name: filter; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.filter (guild_id, mode, rule_id) FROM stdin;
1244403114447212564	invites	1280897162342957140
1195943473409437767	invites	1280906895837888606
1212420500366557264	invites	1280923798383755396
1276605260110237758	invites	1281646459455799316
1281680936316178482	invites	1281711811535831113
1276302538152611972	invites	1282111581026652251
1282717776112517291	invites	1282801540696117258
1282089922517274776	invites	1283188004608802849
1282393410204078141	invites	1284192784827285587
1284532619383672853	invites	1284538669201625120
1121315810892316754	invites	1284652389844127797
1285074886582206484	invites	1286752930321403965
1280513047458484416	invites	1287148470955933698
1288186497585123340	invites	1288193865228095669
949837695050469456	invites	1288947548723220500
1260459692426006550	invites	1289327582927392838
1288335344969711678	invites	1289577595679277197
1264583661932777482	invites	1290804259142631445
1281274638567080018	invites	1291975465493463081
1284579437152702587	invites	1293589089538281577
1232760919113863279	invites	1294138923458760767
1292985929954365472	invites	1294549694214574122
1290409271623946321	invites	1295305020165718058
1151241272326099056	invites	1295755063439921237
1297293375204229120	invites	1297614423027875872
1292154904068227142	invites	1298277976604938261
1298807622484627530	invites	1298816723226460181
1299477839103660052	invites	1299504533357072415
1295820951388422226	invites	1299812024431411230
1291961786852970558	invites	1300662780663435374
\.


--
-- Data for Name: forcenick; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.forcenick (guild_id, user_id, name) FROM stdin;
1270864302877966436	822874120618246187	lube rod
1256851790540832831	1169601140804042842	bro thinks he can code
1271745428584529943	999400198008746004	atlas
1271745428584529943	869990050610429992	The Honored One
1271745428584529943	1245715404085530668	kiffy ni ano
1238888985221271745	1006074392440213595	oo
1271502845161508884	546548675086778398	ling ming
1264118669198233611	432610292342587392	world's best faggot
1244403114447212564	912268358416756816	tranny bot
1275251480487792753	898667446246989834	isa
1275251480487792753	718484602695712860	aaron ml
1275939583124701185	1268741287868235786	nunu
1276761439931203667	792842038332358656	⃟⃟⃟⃟⃟⃟⃟⃟⃟
1271745428584529943	981568350008262696	Bladie
1244403114447212564	187747524646404105	pigeon
1258003767161389087	683272344080220241	an innocent one
1244403114447212564	1035497951591673917	killa
1270486377460404356	1130576619183026287	remove
1244403114447212564	1176490404611379284	#seek tokki (not responsible for any problems in the bot)
1270864302877966436	849639644840460289	gaydes
1275204588894683247	848846505979936788	CorpseParty
1275204588894683247	1261082452579848266	Malik
1275204588894683247	1193423593615392798	Hannah 🎀
1275204588894683247	1135496507940933633	banana
1275204588894683247	1244771947061968910	lettuce
1275204588894683247	1276187064865652861	orange
1153061964633882685	1183890576177909813	gay
1153061964633882685	970210401541320744	alien
1282393410204078141	1267440086673522691	anime (dm 4 roles or help)
1282393410204078141	1099719762487025774	liu
1153061964633882685	738508975955247155	watch out kids! this guy touches little boys and girls!
1153061964633882685	1232778508426809365	heal
1153061964633882685	946350275202023435	this woman deserves to be on fraud watch
1282393410204078141	1232778508426809365	rep 4 pic perms
1173253101906563102	718484602695712860	isas fav
1282563196120727663	1263734958586073141	#1 skid
1285832779216719967	1149535834756874250	/cigarettes
1244403114447212564	809975522867412994	skibidi fortine gamer furry ecat
1285074886582206484	830979440489398293	faggot
1153061964633882685	894275668110622771	peach
1153061964633882685	494262805357395968	gooner
1173253101906563102	1267433174770647051	freaky toilet plunger
1173253101906563102	1166041272927133730	kourtney
949837695050469456	824733526222045225	jjj
949837695050469456	1136100095478206584	wok57
1244403114447212564	1263506520063348836	Poundland bleed
1285832779216719967	810952849398693919	defund children’s hospitals
1153061964633882685	1212661058167246961	lil slut
1285832779216719967	1232778508426809365	/arent
1285832779216719967	1263913303189491712	maria
1290787942687707157	1116267335154683955	majoreta sexuala
1252275415855403080	1276686856536457307	shit bot
1292499075912171673	893080094346723350	qilla
1292985929954365472	1239340311294119957	oyko (protected by woo touch = stripped)
1292985929954365472	914510971928739863	kuma
1291319582983716864	1137873022322233385	bomb
1291319582983716864	1285393945941245965	server dick rider
1291319582983716864	1231997995151528051	riya sigma
1291319582983716864	1276687598907031676	mimi skibidi
1291319582983716864	1149425159254577182	toilet ray
1298459389220622368	1032112629776400474	ray
1056658126180462683	858064570932789248	𝓯𝓻𝓮𝓪𝓴𝔂 degraderzs
1291319582983716864	1253435511377494102	pretty morgan
1290787942687707157	1094285573683945582	cashflow
1292263858412720228	1258893995539435631	ninaa
1290787942687707157	846648342229680138	sclav rujat
1290787942687707157	944592618208243732	uspfrmdao
1291319582983716864	1203756334642765864	Harriet Tubman
1291319582983716864	1244193389487063042	fat fucking retard
1291319582983716864	1278146601512075329	Ari’s slut
1290787942687707157	1244383042353627257	menajera
1290787942687707157	1166362577434062878	menajera fututa
1291319582983716864	1127252153631785021	pretty girl💗
1291319582983716864	1280746666567401485	pred
1291319582983716864	1267122885680697477	best person alive<:rqproud:1298389370914734233>
1291319582983716864	1260479279083294764	ari skibidi
\.


--
-- Data for Name: globalban; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.globalban (user_id) FROM stdin;
407679133603069954
1185934752478396528
1263734958586073141
1182287701186195459
1040983564642169053
1247770987210997793
1247282517288157347
1290698569937981512
\.


--
-- Data for Name: guild_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.guild_settings (guild_id, leveling_enabled) FROM stdin;
1183029663149334579	t
1278389298265194567	t
1244403114447212564	t
1247448738067386379	t
1271502845161508884	t
1260459692426006550	t
1282563196120727663	t
1282393410204078141	f
949837695050469456	t
1288119126602285197	t
1289315449212764262	t
1206215747869614122	f
1281274638567080018	t
1292522369868365904	f
1284579437152702587	f
1232760919113863279	t
1292985929954365472	f
1294870137903517737	t
1287533179166523432	t
1151241272326099056	t
1295818113056510052	t
1295170072372838503	f
1121045839012438027	t
1275243165217062953	t
1291961786852970558	t
1119311424473276416	t
1289787801973428288	t
1302091501479919779	t
\.


--
-- Data for Name: guilds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.guilds (guild_id, prefix) FROM stdin;
1267450090457661474	,
1269931144464306257	,
1153944696788365332	,
1256881462456877076	+
1271453019921190923	,
1263195476245610536	!!
1272020420760965140	-
1272146066946527313	,
1271295719843565589	$
1268305462890205269	.
1254044520467923034	.
1264118669198233611	,
1275486271736774668	,
1271840140381261908	-
1238888985221271745	-
1275251480487792753	!
1253784725672427642	-
1273482259185270824	.
1271745428584529943	,
1272292232250265731	,
1212420500366557264	.
1276302538152611972	,
1278389298265194567	;
1247448738067386379	'
1181509738459037768	,
1268584157639082086	.
1165654249716322404	'
1276605260110237758	,
1279692162954559488	;
1263646900020838400	,
1279837686542368880	,
1267378542874853549	,
1118862694980788276	;
1099977250817982574	;
1257987786888318987	;
1281680936316178482	,
1281980873041772685	,
1274454080286232617	,
1252466052319936534	?
1275204588894683247	,
1275872868114108508	,
1277334651488178186	,
1271502845161508884	.
1282089922517274776	;
1278420379211399249	*
1153061964633882685	,
1157682056277524643	,
1284475167703171114	,
1284532619383672853	,
1282563196120727663	,
1282393410204078141	;
1121315810892316754	,
1271695303921111050	,
1268557160284033107	+
1284715332522479676	,
1284756954933362688	,
1282926708650938410	,
1278894519269589183	-
1285074920627507210	,
1280513047458484416	,
1206215747869614122	*
912657110272213023	nigga
1261480127179653231	-
1265976091319861332	;
1279499166954946591	,
1278315918501351486	$
1285256239520940107	$
1285720473627525333	,
1298398436638326836	?
1285832779216719967	.
1266853535887392841	'
1153678095564410891	!
1253955554334871632	,
1286339518873468980	;
1285074886582206484	,
1266847425084129280	-
1285149906192826430	,
949837695050469456	,
1283124591048527892	;
1284747657377615962	1
1256851790540832831	;
1284592876088463495	;
1288223554197786755	,
1288335344969711678	,
1260827368625279159	,
1289126778086096916	'
1283806216241418272	=
1286215830194884619	.
1151241272326099056	?
1289315449212764262	,
1295584203081252884	,
1260459692426006550	,
1274776424477364286	.
1289274831321174087	.
1227189145051598860	,
1267301925813223434	.
1286694780121911347	,
1279991388808806461	,
965727249108193280	,
1289741574552424518	;
1289951456744706188	,
1290472403763335220	,
1275243165217062953	h.
1290320555668406335	owo
1295531878563971134	,
1291183441857216565	*
1288375552729681991	.
1075834904706826322	,
1279185435297452063	,
1284573817032937522	.
1288119126602285197	.
1262477534482665492	?
1292422832504176660	,
1292499075912171673	!!
1285815171352363028	“
1291976014540570624	,
1281634482918789212	.
1148059997033463978	,
1292522369868365904	,
1287951817971339288	,
1290453711042379807	~
1285735874566553631	,
1284193880379625482	,
1293445012104679454	-
1291211013500178452	,
1277514074506137671	,
1050030051921506336	,
1292985929954365472	,
1294870137903517737	,
1263146753109266534	-
1287533179166523432	,
1244724607584436244	,
1295105048161812540	,
1285855664157233174	;
1268317659037171833	;
1214726898563813406	V
1271624140905779241	,
1295814990590382170	Kpop
1283142907351797850	,
1295649687453438033	@
1279587074386956460	,
1293699972172091523	,
1277519934619910194	h.
1270864302877966436	.
1297293375204229120	,
1219396785982935151	,
1121045839012438027	'
1297636154509885471	,
1271820803167485983	,
1298807622484627530	,
1298459389220622368	,
1295820951388422226	,
1183029663149334579	-
1299313023617466419	,
1299477839103660052	$$
1281840879308636253	.
1290702553960681512	,
1289787801973428288	?
1299011532465635430	,
892675627373699072	.
1298932833804619827	*
1295506830952366091	,
1291961786852970558	,
946800234804166697	.
1289990098649088111	;
1301221390388822038	-
1300098373793087539	$
1212871770571407410	:
1256068630987145298	'
1236667753755181068	.
1300904358061277224	,
1228003068088684584	!
1119311424473276416	,
1301284604615069778	;
1223076914542153768	izo
1224770474257678356	;
1302091501479919779	,
1231168248075128843	,
1292861168054046831	;
1282346503997886565	.
1244403114447212564	,
1234621599420776550	,
1274164559296335922	,
1276761439931203667	,
1296674979714170921	,
1299880499644334200	,
\.


--
-- Data for Name: invoke; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.invoke (guild_id, type, message) FROM stdin;
1244403114447212564	unban	{user.mention} was given a second chance <:awkward:1273676311281532958>
1244403114447212564	unmute	bro was unhushed <a:menacemonkey:1271184769836912680>
1244403114447212564	kick	{user.mention} got ejected <:madcat:1273037748852363314>
1244403114447212564	mute	shhh {user.mention}
1253955554334871632	ban	https://tenor.com/view/tommy-toskonaut-tommy-toskonaut-tosko-tongues-gif-22622185
1244403114447212564	ban	https://cdn.discordapp.com/attachments/1244318491645968444/1250881996151062712/caption.gif
949837695050469456	kick	cya soon loser {user.mention}
949837695050469456	ban	https://media.discordapp.net/attachments/1104463146246230058/1261746752009142333/attachment.gif?ex=66f1af3b&is=66f05dbb&hm=c736d7cdb82bb5c4721a3a5776e3267c243b830dc930022959f1994813a6d39e&
949837695050469456	mute	https://media.discordapp.net/attachments/865258056161558528/881884440383614976/image0.gif?ex=66f164e3&is=66f01363&hm=26857f34619cd8f44690058604c339d4777083a344d937861b1b7ac4fee3a3af&
1253955554334871632	mute	https://media.discordapp.net/attachments/865258056161558528/881884440383614976/image0.gif?ex=66f164e3&is=66f01363&hm=26857f34619cd8f44690058604c339d4777083a344d937861b1b7ac4fee3a3af&
1292522369868365904	ban	👍
1292522369868365904	unban	👍
1294450257211424828	kick	{embed}{description: <:banhammer:1294869722902433846> {user.mention} Was kicked from the server.}$v{color: #ff0000}
1294450257211424828	ban	{embed}{description: <:banhammer:1294869722902433846> {user.mention} Was banned from the server.}$v{color: #ff0000}
1294450257211424828	softban	{embed}{description: <:banhammer:1294869722902433846> {user.mention} Was softbanned from the server.}$v{color: #ff0000}
1294450257211424828	unban	{embed}{description: <:banhammer:1294869722902433846> {user.mention} Was unbanned from the server.}$v{color: #ff0000}
1295584203081252884	ban	👍
1295584203081252884	unban	👍
1295584203081252884	softban	👍
\.


--
-- Data for Name: joindm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.joindm (guild_id, message) FROM stdin;
1244403114447212564	meow
1279185435297452063	make sure to join discord.gg/hexshop for cheap followers nd shit <a:bear_cheerlead_dance:1279431766368849980>
1292985929954365472	rep /parkk<:31:1293051875339276411>  for pic perms + boost<:role_server_booster:1293051324749058074>  for roles
1232760919113863279	make sure to boost n main **<#1294023945573498900>**, thank youu !!
1290453711042379807	set wlc to blame*!* rep and boost for pic perms!
1285735874566553631	**hey enjoy the server and make sure to join the backup** https://discord.gg/DWdGJPZx
1294870137903517737	this is a private fg {user.mention} be close with <@929503912728334407> or dm him<:0000quote:1267509366957936712>
1295531878563971134	don't forget to join discord.gg/hexshop and discord.gg/arrive for cheap members and server boosts and much more!
1222897124073541673	this server is no longer in use / join discord.gg/xioshop <a:plsss:1256562150000820285>
1291976014540570624	boost+rep for perms
1279472645661917347	main and boost chihiro for roles <:l_tiktok1funnyface:1296944721146548255>
1298398436638326836	**willkommen auf habibis!**
1291961786852970558	Incase u leave discord.gg/bounty always here  owned by <@1286072791325478988>
\.


--
-- Data for Name: joinping; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.joinping (guild_id, channel_id) FROM stdin;
1244403114447212564	1244407962756321402
1244403114447212564	1271137690649231423
1244403114447212564	1270761684285390979
1271295719843565589	1271343117844611105
1272292232250265731	1272292943591374891
1274467574842658928	1274475191405383812
1274467574842658928	1274476317961883658
1244403114447212564	1275776609944862850
1281980873041772685	1282053666668281969
1281980873041772685	1282054456908976249
1275204588894683247	1275212833264500817
1275204588894683247	1277780890495483974
1275204588894683247	1282388444269645936
1274776424477364286	1282895744747180102
1099977250817982574	1236827663465840741
1284532619383672853	1284533745000517674
1284532619383672853	1284533508836163624
1284532619383672853	1284533524657078485
1284863818073112616	1284863818694000712
912657110272213023	1287023447238770699
949837695050469456	1287441806136573993
1274776424477364286	1289685232127180912
1279991388808806461	1281350740568444928
1279991388808806461	1281351350520647771
1279991388808806461	1281627236423696477
1267301925813223434	1281244659879776288
1267301925813223434	1267310404552495125
1293699972172091523	1293708129657294868
1293699972172091523	1293709451202658400
1284579437152702587	1293752324312924243
1295584203081252884	1295585392875274290
1295531878563971134	1295532235067359284
1295649687453438033	1295748669609345095
1295649687453438033	1295714360190046248
1295649687453438033	1295649687902224496
1222897124073541673	1268381757145874525
1279472645661917347	1279509158789644321
1279472645661917347	1288761263446294538
1279472645661917347	1279502612688801803
1279472645661917347	1279509209339265045
1297293375204229120	1297296118329114676
1296538895030161448	1296820568812945418
1296538895030161448	1296820775550193746
1296538895030161448	1296821779389747321
1298398436638326836	1298398438328766475
1274781210475892756	1299351613978443868
1291961786852970558	1296927860426014781
1291961786852970558	1300639257416831048
1291961786852970558	1300665143272935537
1291961786852970558	1300643523670048778
1291961786852970558	1300636163379560489
1300904358061277224	1300904358061277227
\.


--
-- Data for Name: lastfm; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lastfm (user_id, lfuser, mode, command) FROM stdin;
960101203881103402	haruyt600	\N	\N
1175195486605561887	vxkl	\N	\N
461914901624127489	ul14	\N	\N
1211082272393138237	turntmars	\N	\N
546548675086778398	solixblox	\N	546548675086778398
1233417695974789172	uhhframed	\N	gay men
919674489581731842	twrblx	\N	\N
605995776711327769	SnarkyDev	\N	\N
1243274323402293259	precinations	\N	\N
1272545050102071460	\N	\N	psutil
211069788544434178	designer1337	\N	\N
392300135323009024	x6urr	\N	\N
394152799799345152	davidosxo	\N	physic
1250382435632418816	elleqe	\N	\N
809975522867412994	kisakimeowr	\N	\N
269910607174696970	lucky 1	\N	\N
627991951857418261	xrm0s	\N	\N
716056869164285993	ReealLion	\N	\N
971464344749629512	fijicold	\N	\N
617249450867425301	vespier	\N	\N
1143632676822192249	corrupteddwoll	\N	\N
1140301345711206510	xqccss	\N	heal
598918481257168936	DollaSign5	\N	\N
153643814605553665	jercking	\N	\N
1280856653230505994	aiodns__	\N	\N
1153344923463069756	cxxyynn	\N	\N
713128996287807600	waisersef	\N	sex
1208472692337020999	Bruceboy_YT	\N	\N
1278250011431534593	rayzen_6000	\N	\N
971064130704400405	slimepointe	\N	\N
1189492237130797167	<@1189492237130797167>	\N	\N
1185934752478396528	fetchrow	\N	meow
1288323990842249246	rapetron	\N	\N
1286715329682341936	koski1222	\N	lol
1011724934831149169	MathiasTyner	\N	\N
1083131355984044082	StoleHerFunds	\N	xio
1209096114947498035	jig	\N	\N
1116267335154683955	Csmn__	\N	\N
486354752301432838	conwaytm	\N	\N
846648342229680138	d1nisa_	\N	\N
509799055438774305	alecs1006	\N	\N
710993692764274728	editzbyowen	\N	\N
999160997711458366	\N	\N	?set
871861410659971102	redsusnotme1	\N	\N
187747524646404105	onedeals	\N	\N
942337823271424001	\N	\N	shiat
1271796878555484222	xlow1234	\N	\N
1204683623744282656	roobberttttraw	\N	\N
1165355330880933972	.kissestosey	\N	\N
954854246753370182	\N	\N	https://ptb.discord.com/api/webhooks/1295967698957893673/-OZuNAIBx6BH-0xv74zXzynE8AfFxQbqNqouLPSp35GZPHGh-8Fq0NQyojmYkdH-St4m
1122984949541257337	ecstacyx	\N	\N
1095015244264386630	\N	\N	<@&1293876317187477545>
241568842344562689	\N	\N	xio
1187497523473039420	\N	\N	\N
606569668936728639	fppb	\N	\N
1256745993215410218	w7ru	\N	\N
574429626085015573	fooc	\N	\N
1252343511571759149	Cryz	\N	\N
\.


--
-- Data for Name: levels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.levels (user_id, message_count, level) FROM stdin;
1272545050102071460	1	1
545396542597759012	3	1
1040983564642169053	1	1
1251576059405664311	47	1
1261733744713138197	6	1
335500798752456705	1	1
1057537400135483464	1	1
775812932759453746	11	1
609451852878315541	1	1
1053708987696173148	187	2
235464874149412864	1	1
979467336329338962	1	1
1274288825367269469	11	1
1264003756081545287	6	1
788731226504691713	7	1
907551408985890847	7	1
690628646527959111	4	1
1254807901596291132	12	1
908356374294048799	20	1
716508567615569951	2	1
1274540031578603550	125	1
960044945383759872	12	1
1074668481867419758	861	4
1153880579738189925	2	1
1257453783714365553	3	1
1269364087553396911	2	1
1126212889473196242	2	1
513332423124058132	3	1
962501581083902062	3	1
629401979361427477	2	1
864368445893378078	7	1
1275926585588977757	1	1
1222157774096699516	10	1
822560172085084271	2	1
1225304033711886451	2	1
1160045635114905640	1	1
1129584253806575706	3	1
547235734839361577	11	1
1172682555896647750	1	1
660749429300658217	15	1
1226403301348741155	25	1
627991951857418261	30	1
1150482883904020570	23	1
477105109482864642	1	1
1153676881653157898	101	1
1016501408691933184	35	1
1104070437060759634	1	1
1117638478176464897	2	1
1255989555115589672	18	1
1254567013159010335	6	1
269910607174696970	33	1
1111589272810696725	1	1
639591691468275732	20	1
1102070464387493938	3	1
1269597022634119261	1	1
1231889211888631888	53	1
360037283581263882	2	1
1264568492640829441	12	1
594035565834403841	1	1
368043889979949056	2	1
886064023039246377	25	1
813287269947539457	6	1
1152719097566597190	49	1
1110199322643021824	2	1
1214707668099272884	1	1
970769009811280032	25	1
1251138585789337600	44	1
1251329834467070083	3	1
546548675086778398	178	2
1016429230483054612	2	1
808934375118864385	70	1
1280584295542423734	33	1
1161772932335403119	1	1
807387522543124520	292	2
979450729762816051	330	2
851627132681584680	245	2
926206867645018172	1	1
1152968028640780470	6	1
1109135114727870535	107	1
993037306485289000	3	1
611339099122434062	298	2
957771692300709918	8	1
1184464718862237798	7	1
664676280683331587	12	1
1221642249608364175	16	1
1051977049746714726	107	1
886703026029613057	27	1
1268467834460176415	76	1
1124996360131854438	2	1
1208306258541678625	63	1
1261648918253670554	2	1
964590877131554927	14	1
772966218466197505	87	1
1254503253568389251	7	1
717099731301695549	5	1
735217154772959303	1	1
1068734540136329227	14	1
999881692493922434	1	1
1133613152622366861	1	1
1010023575341772800	1	1
1240795779954769963	222	2
1252001166703853588	4	1
919315551099162694	38	1
919674489581731842	27	1
1253766968813817958	16	1
1180873730033991911	7	1
1004684571239002173	333	2
1183890576177909813	3	1
718252241274011649	3	1
1008008103880560681	52	1
1083861728380584038	22	1
345462882902867969	18	1
844970791689912360	10	1
660052612384686081	1076	5
524730187967889428	396	3
1263420943267528816	1	1
1268730681069146133	64	1
1076214676402229289	12	1
879893182819762197	4	1
1028477940603813898	4	1
1280195504596058254	9	1
971138473924911194	2	1
1005331868276768848	5	1
1257438474605301832	1	1
1060059596934352926	1	1
598918481257168936	97	1
1149107727755382785	120	1
1059935026311086131	9	1
1030100913861439588	7	1
495613453948551189	24	1
461914901624127489	458	3
1214236482097909862	36	1
1099719762487025774	262	2
750379503179661444	194	2
855730545727635456	86	1
814652188323348480	180	2
1244699497209270368	2	1
1100962676756185120	3	1
305519747078946818	1	1
1254368047238479922	3	1
976429429041557575	106	1
1278066431510188079	117	1
1239422040549888070	3	1
732530644412006460	241	2
1234025578232025122	70	1
725954230401105991	47	1
664370511421374484	7	1
1070834009266991124	136	1
1113915302326059030	50	1
788565247203999744	65	1
311842023835435012	341	2
1206141215725326377	11	1
619643978261725215	149	1
1267440086673522691	888	4
1189775750287605820	269	2
1110782784349425664	923	4
392300135323009024	54	1
1246380245272231987	6	1
1251030413359583266	190	2
875096125588262914	852	4
1167775097990430741	5	1
1260751081454043169	2	1
1259709597694824469	22	1
1209220182426394634	767	4
971464344749629512	89	1
1190898714001281074	39	1
1115373972385714196	99	1
1279589132829720660	10	1
1134251547220512830	476	3
1193285541282721904	538	3
1254985571181396071	123	1
1188955485462872226	106	1
875439738088210432	762	4
945427441889984562	17	1
1277330614122451006	163	2
153643814605553665	509	3
1212261249996431512	437	3
1102353315334983784	1147	5
1243223915422023750	14	1
826218685785047077	2156	7
1010919763230339102	374	2
1224181187514339410	211	2
1251364360518107227	470	3
1003450896950235247	1	1
863332796655468545	3	1
1264834826389819394	1	1
737153352349122613	1	1
1280249216802885715	5	1
1264940328515932220	13	1
818854807476371497	64	1
1255612726718500864	49	1
831686991896772638	14	1
1203478238329049129	49	1
1175195486605561887	281	2
1057056108340064346	7	1
864300900151722004	286	2
1279830524424097855	3	1
1277685351779012810	3	1
1203862143032885368	26	1
1203317846650912829	6	1
759174420555366443	3	1
1188976669843804230	39	1
1234200316602224741	9	1
1141124521722663023	520	3
1111864226089271316	2	1
198883880634155008	19	1
1234330289472536607	21	1
1092591212629856280	2	1
1173121628457156690	10	1
1204634271453548635	2	1
1233854190078398565	2	1
960101203881103402	10	1
1186426593179074581	20	1
1079530734341083229	30	1
1277003340475142146	5	1
1271343572263764120	14	1
806184013873545256	23	1
1059626355324620900	95	1
857315654834192395	1	1
643827079150043147	2	1
973708152287670282	34	1
990119557194715176	169	2
1111973162742190160	46	1
1244557936907518059	5	1
1050213710179880991	34	1
960683557485936701	1	1
1275642082064863325	205	2
1175814484217045032	2	1
1010384772951969856	1	1
1035497951591673917	4874	10
1107915069506994349	26	1
1014880096353517699	4	1
1130285145249808534	3	1
991413994709590056	114	1
1259443225542918218	190	2
929860691408588920	5	1
1254008690671882283	2	1
1108144473558483025	29	1
1273025581805736057	2	1
841753928693317642	40	1
1194519294202101781	19	1
1230266854212243471	2	1
1098118649786675251	3	1
1050189870695460925	4	1
1134017951108972628	5	1
1205224480046321764	9	1
975067687074025574	24	1
1116006308387237940	19	1
787081570469150750	113	1
1232865680991191061	15	1
1150929140971737179	44	1
1227659291008172165	5	1
1083200951634116749	391	3
1148648231459373208	1	1
988469942200463370	1	1
1250382435632418816	4989	10
713128996287807600	533	3
1272550773850509344	4	1
1001638971144671343	39	1
1211208584201904249	4	1
763951918169980969	40	1
948859560423194654	48	1
829289684722122782	1	1
775892463519793173	27	1
1162552427686416414	32	1
1153047993453383680	71	1
1275188136158171147	36	1
1194843544112865312	21	1
1205893602090422302	26	1
736674516482129991	32	1
1206276040939282494	46	1
1105256158777839728	30	1
522470549713322020	28	1
724726914782068856	33	1
942509642725081088	34	1
1043237783260639272	25	1
994843851355324447	31	1
1226587423337873433	28	1
655386817549303828	78	1
1127935158952149024	4	1
1235591552202702868	178	2
1148404261567336609	7	1
1126642036414619698	4	1
1057345675559456858	1	1
1170877573614538833	1	1
1092515201464676373	9	1
1253778659865526364	40	1
1199019416780812408	80	1
236957169302372352	1	1
574429626085015573	105	1
772833610105225237	32	1
1240001373542551618	68	1
1180907331819675705	7	1
1234674028493672478	1	1
1067993009439903774	2	1
929150986793156628	51	1
1241383790555693188	2	1
1276111747694067736	51	1
1033813242331529328	35	1
759124497704943617	25	1
1262506390124101724	34	1
1194737299645288509	31	1
1124526209292832888	32	1
725446285456441475	29	1
1251284202557804634	30	1
1109565939772559360	34	1
1177281199534772350	25	1
1075444616876265583	8	1
638992618637885440	8	1
147525074201739264	5	1
1279462640313176076	116	1
852784127447269396	52	1
1210211190379388952	42	1
1082976686846509086	190	2
596752300756697098	174	2
1262943338340945920	13	1
1110785202558619689	1	1
736478638761050173	1	1
809975522867412994	11244	14
1208490323622494293	156	2
1275925200130805781	140	1
536773521301307403	53	1
1247076592556183598	162	2
690715731016548394	4	1
1195148145647177869	70	1
1260736524035817595	29	1
1204863605405651008	422	3
1165324138076971018	317	2
1101181298472669194	167	2
966249539235352596	77	1
1214676956952399974	19	1
318294513690869761	156	2
1278250011431534593	19	1
1177497949601812512	30	1
1208472692337020999	3806	9
1084291705005674527	57	1
986506709210107934	9	1
1202022660138074223	1283	5
953107407280676885	64	1
1076218266416054293	8	1
1228236906697850891	185	2
1135094868717338717	5	1
707313140349796412	12	1
320419193172393985	1	1
1222159416795861047	413	3
919125120616898561	32	1
1082349488246636565	112	1
1168186952772747364	65	1
1226376084996620380	3	1
1055447291059765288	11	1
1057447446084583494	16	1
1117229232892936233	90	1
1079119607467622422	65	1
820745158323994635	1	1
1076669383524487168	57	1
492421342659084301	48	1
605995776711327769	82	1
1267726635126358048	7	1
1273201960685928468	4005	9
1128015060669829330	49	1
1082206057213988864	545	3
394152799799345152	7948	12
1280856653230505994	627	3
1233417695974789172	328	2
247801829570772992	969	4
1140301345711206510	3543	8
984523287197532170	97	1
755265955583623179	1	1
1286338493160624180	11	1
1176361126578094080	1	1
1183219072180162625	4	1
1258029431037886547	32	1
847281692338683935	1	1
721731295603982419	240	2
1263716331941920778	81	1
1151121867508306001	3	1
1200632542148165714	4	1
1190958476936097945	1	1
1263629764850356237	4	1
410887200436256768	1	1
1118784810706538577	3	1
1282904449592983572	2	1
1214830500041072701	1	1
801882083169140798	4	1
1250428931711041609	3	1
763141886834769980	3	1
1169253526673817613	2	1
1128517450376429648	1156	5
1014093357867356190	7	1
1127324270364737556	69	1
1046726475077922866	1	1
1268696727443996775	2	1
843188476400631868	6	1
1239534068379553802	63	1
372830774296182794	12	1
850305198693679114	2	1
973691324186386502	210	2
1068185631768969227	6	1
885525211435397160	5	1
754315010624323655	3	1
1098220364502401085	2	1
1050696828070400051	12	1
601873958891028510	14	1
806043187973193728	3	1
975393549212319744	28	1
838855989804924989	26	1
1207108276517605411	96	1
731312838085181470	5	1
891003652528021535	16	1
1056378117603725403	44	1
1188570797263036437	72	1
954563508576595968	3731	9
104703632485670912	12	1
1253394430652846151	1	1
1148114962561126461	4	1
984491162737979462	2	1
1270184590375387168	64	1
1286752191042031638	25	1
1094762779728167024	1	1
1268361596854603873	9	1
688841496086315071	8	1
1156491706234056714	1033	4
1106632181272563822	2	1
1006569596100292648	1	1
729897248044875837	22	1
1266529966695120997	1	1
1282763280699359283	2	1
1092087030240006329	1	1
1011773495052619848	8	1
1267903638538555454	70	1
1170466681924100119	4	1
991410597176541304	61	1
1284285569677004873	74	1
1116267335154683955	22	1
991750984881688628	39	1
1203913917546504225	5	1
1238767909568778280	18	1
1286178177869287434	16	1
1191436827400351755	357	2
425343562893492224	6	1
1274496968391004193	10	1
1280882354478645250	150	1
1181492051167158272	27	1
525041191092224024	2	1
842499501192904766	27	1
1276454642976292887	1	1
1182377641857273918	10	1
765664542021517342	8	1
1012141143665954816	86	1
1206782090037952532	29	1
1261462777986551819	86	1
643573925778817035	133	1
1092881600343191723	2	1
802116541285662750	140	1
1202946331325505546	9	1
1020741657097949264	2	1
1188564358398230579	196	2
758171266288582676	6	1
1244257703895760986	3	1
1161017807564193832	1	1
1285060745046003796	263	2
805205334816981023	22	1
1209513687338192926	1	1
1222362291358531684	1242	5
1173768493057978383	8	1
410975778331820044	4	1
1195393847707058276	12	1
1232834461385883651	74	1
1136100095478206584	1538	6
671033850520141824	2	1
1065661018879053965	5	1
1269455947265478750	36	1
1192935870135795776	752	4
1247387601858723920	232	2
510231479436050452	2	1
1286715329682341936	1479	5
526188409320898600	22	1
1033650126562009108	130	1
657698370621538304	19	1
1010075851049668660	50	1
1057491043345502239	294	2
877490743944544296	11	1
1212151649213091913	31	1
1176305975083417682	4	1
1249396589043253309	13	1
1257647004272689162	12	1
1148078794863820810	258	2
1083562632449101925	968	4
1268181424704585741	455	3
1256692841166405815	4	1
1254429657797890062	2	1
1243289663280775321	31	1
397027584451543050	2	1
1081907165100519514	227	2
953736859870171156	125	1
392020211789725698	2	1
1290698569937981512	4	1
1068602174688460800	1	1
1051021421859569714	1	1
689726676438876252	19	1
1005135934028775474	4	1
1249695903644647479	2	1
1051903023154221057	2	1
876152866434342953	21	1
1281413147042779198	2	1
1176490404611379284	2852	8
1290677932607672379	1	1
1247282517288157347	122	1
1100835956631810188	1	1
1187987535318761576	5	1
1087318581680803911	3	1
1207108189884125224	17	1
1251235832099110936	73	1
1217376690578391107	41	1
1286489325697241118	217	2
922082461201076287	1	1
831953870133133332	5	1
958786815484129300	3	1
710204523909480499	1	1
1280368650896801816	4	1
1289371559814762516	55	1
718174141340975208	3	1
1120595636681707570	116	1
1200328483029655615	16	1
1107903478451408936	2	1
964705479668400188	5	1
391090595067723789	1	1
1143952663952769095	4	1
712788199398703154	170	2
1259762368125206600	84	1
1166516904219906193	2	1
1270373805256212481	166	2
1158896482909438062	10	1
1185934752478396528	2281	7
666019644297183234	15	1
782824698320126044	33	1
1262799073077891155	38	1
984521925978128475	248	2
1243274323402293259	1474	5
1022554573828792420	843	4
1237504181678506040	166	2
1164864602664882252	378	3
1038750693948936192	373	2
768561255446741012	183	2
1147980154749075557	10	1
643054595983015977	30	1
1036203429892194314	115	1
976313795733516378	146	1
1118013320369287210	1	1
1195812064288047318	1	1
1195812137696755866	2	1
889451371647082506	1	1
1263506520063348836	8	1
1104119396139532299	1	1
1212132082638397440	4	1
1277908376906502270	1	1
664534827449712641	3	1
810952849398693919	40	1
942998929509855283	3	1
914313568495742986	3	1
1083131355984044082	1986	6
1139622774789382175	2	1
389538973510533123	3	1
1286879416336646155	1	1
936532257827598376	1	1
760568244934803478	1	1
719903204690624512	2	1
853034806308765716	4	1
1188520772558401630	5	1
857645752473223168	3	1
1090612419715399730	3	1
1155434966042280046	2	1
927344394451976203	43	1
845494568341733407	136	1
1262157294670708806	38	1
1241414067931971606	37	1
1249410329168056350	7	1
1284840070024663051	2	1
787327247941632030	1	1
971064130704400405	272	2
1277089739446550588	1	1
1271115872714489877	1	1
315899725314523137	29	1
1259106624795185152	2	1
1189492237130797167	6	1
1146074543086116984	1	1
720405553075060748	7	1
1277763769606340632	1	1
950899614184247346	4	1
1156382549375983627	4	1
954096585640382485	3	1
1281680068053307433	723	4
1260955952442773595	114	1
1232581120227414076	1	1
1248844854130118759	1	1
1237976101121163266	1	1
414109733541249025	1	1
797127178202251274	1	1
890441637602410506	1	1
1253462062353350699	5	1
779521506820489286	3	1
1138582022361718894	1	1
971476514929520692	2	1
1250843966350295112	43	1
877782086528950312	1	1
472849121947025432	79	1
1245837128420819146	12	1
1201110167400493168	1	1
763930368235012117	43	1
919075325042888744	1	1
1239814666994319372	1	1
255841984470712330	1142	5
1051585717039530014	2	1
1214535415772483614	1	1
1267902139188121782	1	1
1179107565586628631	35	1
1167696769950416938	4	1
1278386755653075060	10	1
1186169430703616060	1	1
1209096114947498035	223	2
1270243158625882125	1	1
1200457190553682034	2	1
760368146153734175	4	1
1254638784755142728	51	1
1182318024120873033	4	1
204625571865427968	1	1
1228454672340090912	104	1
994009947543179325	8	1
1272212846297743423	1	1
1125459509654081636	4	1
997012189804232734	7	1
475131299603152900	22	1
1117289608321978462	25	1
993482477643497482	5	1
735804263422230539	1	1
1151660279118172160	2	1
969002370463858748	67	1
1271318631984267317	142	1
1064714658268840058	158	2
864098438559039538	3	1
1208342965676937236	122	1
930168202892292096	18	1
1206244004963024929	9	1
1258933647709438026	8	1
1254805358225129536	146	1
808717785676644354	20	1
1249121430172598313	1	1
969653373097885736	18	1
1096447981718343810	1	1
1058276830194438224	1	1
823982725684920350	2	1
1182596956787331092	2	1
474206995214368779	42	1
1291368329403043952	1	1
1234808559276003349	33	1
1289601134188826734	1	1
929688171363586048	3	1
836361426531516459	20	1
816464553842966548	281	2
1189987703811477605	1	1
1242155320986570829	3	1
1081325935690793070	7	1
1258409203748442206	3	1
1277626614305394768	7	1
458546741285748736	13	1
1253339405901500456	2	1
1091559622269210685	3	1
660885593911459840	5	1
1228378191458996286	2	1
1101777735866650655	124	1
1284026529226948663	2	1
1258415902655905816	3	1
1207361971301654542	2	1
753723327499075732	25	1
1257791875449094148	9	1
1249781749232173090	1	1
954883120119820390	10	1
111540637714653184	17	1
782559059999064085	35	1
891155740008542209	17	1
1111715731244077147	20	1
801500472178507796	3	1
1189347827520913472	1	1
583376655410790421	393	3
1143190246561947708	9	1
1254107837718724640	295	2
1216791900300902543	21	1
284842915577200640	237	2
1255332128015650839	148	1
1057214315083603979	3	1
1038873833605709824	2	1
1280239413804269720	2	1
372354102601973761	2	1
1214599933852651560	8	1
1281061217384792186	42	1
612124076445794314	34	1
966233134553251840	28	1
1268741287868235786	1	1
982459630527610941	2	1
1243223875186331658	1	1
1094306053895766056	2	1
910845169312595999	1	1
1008793439460151307	40	1
965622044937044050	8	1
1010821439252865094	21	1
824251595830984735	8	1
857325231525330945	81	1
873112287421026314	84	1
755324667547353098	78	1
456970429668524033	41	1
1197847794048843807	37	1
805431415658512415	54	1
801580789866299392	150	1
1174802725934993511	3	1
1209634819429109770	277	2
1184517119321313381	60	1
1286065140864913450	201	2
1276740071218876684	22	1
1215424258621046824	900	4
1207108231571439636	12	1
1184991444755288125	3	1
1283227297629081674	2750	7
1257797282582106155	23	1
1053100671525732352	304	2
1154065198538305686	252	2
1246491732992851968	47	1
463409172298334209	73	1
1011450038775455836	89	1
1173899303773806621	6	1
1288745438027055117	98	1
1237801023863787683	14	1
1122388514789662730	6	1
1063764585435365406	1	1
1268407079253577809	1686	6
1206515833333878796	2	1
1193453678791757894	1	1
1251454341743644694	1	1
800895629744013382	11	1
764597298357075979	40	1
1261527992342151170	76	1
1170607885861011521	7	1
1276194569830137998	1	1
1194925782989017153	9	1
1183358023213776917	27	1
839748487851147294	3	1
995462178998063194	20	1
990944154068602895	6	1
1204271887358889996	19	1
1199771404506243193	1	1
1145178430883774464	1	1
1187515891294945352	645	3
1265471925057093785	312	2
730353642372202566	2	1
1292243100517011549	1	1
1099358934558588938	2	1
981604164532596857	4	1
1179251989616525436	6	1
960573982879399968	4	1
1280569215471980564	1	1
1247743961909428316	1	1
1240661769454878762	1	1
963886694246010982	43	1
1209968571938115675	30	1
1187528296137773127	38	1
1172641524614430870	45	1
1289221701841850389	2	1
912193359093854248	55	1
393618593633533962	1	1
750789100835176463	10	1
1171311287825879107	1	1
1167911246641758360	12	1
891749870405312564	1	1
731935983389638739	6	1
1122257448623935599	1	1
1265913442624340100	1018	4
602811941307678741	32	1
1277567752202359007	14	1
767357178217627688	199	2
1199766647762845796	10	1
397257206342483974	11	1
1242279983175565323	6	1
952715352301785203	10	1
787905982427693072	167	2
1112425309153800214	116	1
1270511719386447955	3	1
831899413315977297	6	1
1041083671391780864	8	1
955899315220525146	10	1
1288233229169594481	19	1
1242619354844106752	14	1
1268506398032134167	1	1
1126615928126308353	1	1
1003373004597768296	31	1
814542948645601330	3	1
864769441552269312	1	1
1270632281291227215	6	1
656678284771459092	2	1
1237875782261538816	181	2
840711000248418335	37	1
1288079063797469215	9	1
1219248857318424721	319	2
1201416025363730538	4	1
1278866835735056424	3	1
1031614578787897437	1	1
1268137754659655715	1	1
971782093912817694	7	1
1121589146851479673	10	1
1211082272393138237	341	2
1265801235911671839	390	3
788828950226534440	11	1
1284701337639977060	10	1
672936576958857238	18	1
1146976854243282985	58	1
840604992109150228	2	1
397524610394095626	3	1
1278475075728969873	819	4
1224810144345358498	7	1
1155191354729713684	81	1
1265383601105535058	1	1
701276592848240712	94	1
1277439339764383766	34	1
1246580805971742824	6	1
1277766989162479681	32	1
1235492184652779520	194	2
1271193749254443148	131	1
730625463373791302	1	1
1202449554277015635	619	3
1239340311294119957	798	4
696263273795944498	564	3
1280790304672186389	549	3
1291943460013735967	31	1
1144677139497635880	744	4
1049618225882734593	1262	5
1290465797830873112	4	1
1284696442753122327	1	1
1284388538087116881	2	1
706675291728117840	10	1
1285412783676063786	934	4
1254383828005425175	29	1
1271914563541008406	1	1
361841263013789696	2	1
1287337045509017644	337	2
1081799799700983869	1	1
1189322376245157899	49	1
1129385648843931658	51	1
813464823542710373	9	1
1207010082735530046	166	2
811491848907522059	15	1
989965374562926642	32	1
1083347340364091393	4	1
1214787623420428308	13	1
993543074699542559	1	1
932816796568915980	1	1
1205023979044339742	1	1
1239272794894762094	1448	5
1119705845341618356	6	1
819965577828892722	1	1
1291170490790051938	351	2
803467210789748737	9	1
1265661398701314090	100	1
1267612114231627776	113	1
1200893579485253857	9	1
1276670564487925824	1	1
1283025289529659472	5	1
1184079224018051148	2	1
763081790746263582	1	1
1236732536806182953	19	1
999352355466260612	8	1
1153482236222509087	1	1
1252833101709836310	5	1
827169615909617665	2	1
1081505411154321430	1406	5
1154184323625390110	1	1
795882673091903488	151	1
764838333905502238	25	1
1075992840192131123	1180	5
1117582353330614312	1	1
1048153939121549312	262	2
1079992327784910860	13	1
1249228808360300615	1015	4
1275854277872713817	26	1
1285267964538654750	519	3
1163102771487195247	1	1
1275919358014521406	29	1
1078673864915165356	1	1
1133623549563768832	2	1
1180783899945742397	72	1
1044450189139775519	3	1
729105995246076037	1	1
792838801319788594	6	1
905572359853965343	13	1
1242617739432956027	1697	6
1239298204324073583	1	1
1176766526553067572	1	1
1175268530250330222	117	1
1043694442181296129	219	2
838628580161880085	6	1
1113909488169271366	54	1
1271360685942771713	112	1
880180250158444595	28	1
933118018270138439	7	1
1190927233590775882	4	1
1263737585180868711	867	4
1182060156058619964	533	3
1236069013042233346	48	1
741504327943716915	218	2
1180347533185257502	244	2
870960945889935370	96	1
1266181017396580415	25	1
789910732275843104	8	1
931100652942290954	22	1
950910798048419871	81	1
1292640107555454988	17	1
189975532287295488	20	1
1254355023341682739	136	1
1292141895807664211	170	2
1273059341238272001	3	1
962491771575738378	18	1
815640687466119228	7	1
604275638974545930	84	1
1289336605966073856	2	1
1204376809987112992	6	1
612934343685439519	10	1
963269210874740786	9	1
967445387151564850	1	1
747127749184847932	2	1
1288518258756161668	1144	5
1145070351299133531	128	1
1267615219778195468	749	4
969418223210606612	2	1
1264602748771635230	210	2
998033811331874816	75	1
740568519992803399	3	1
1069051615576866867	499	3
990093088032718878	16	1
1291461208297177150	10	1
795099082661298246	334	2
1283029104924430421	4	1
796447052074188890	54	1
1210307935268507682	155	2
1208322906984288276	34	1
1291232902197284936	9	1
1182667780030468127	5	1
1194437488207470714	97	1
837306192409395220	4	1
1227038131493273690	65	1
1060001047583666289	3	1
1185382674009956454	13	1
1197055174427033643	30	1
1269526226876235779	544	3
1237662181114249237	17	1
1218811875320660039	587	3
1263241230985461801	2	1
1098628628901806214	6	1
741757515297194014	4	1
877362388985335849	68	1
776693480889909249	1	1
1074906343531610172	124	1
182899377432559616	1	1
668143732977172520	282	2
1227630554636095528	50	1
960228200238174239	1	1
1185232222563860562	2	1
1219040562527604782	21	1
1163293954494697614	10	1
1089941438059524116	12	1
1268399253982810189	14	1
994354886495973502	17	1
799092974902181930	3	1
1095751142346080370	3	1
781181040177184789	835	4
1281538661741236267	242	2
722571496555413564	14	1
714994658442477598	1	1
1196932542591418528	10	1
601608984813764609	2	1
1253994148554604588	47	1
723650152711192657	15	1
1130303460353527941	34	1
1119667810130481212	343	2
1192961461211906170	1	1
843058343555760138	4	1
1034964142819377152	5	1
723630094374928395	15	1
723630014498865283	16	1
1268089360146890836	31	1
723582273173192797	14	1
1163046855542841365	4	1
280994601152675840	17	1
1223145513289912366	35	1
984947525234610196	1	1
723691783527333888	14	1
1290385049262227497	1	1
774661602183217152	2	1
914510971928739863	54	1
865054672401596446	1	1
1258389064999239761	1	1
958891391876993045	1	1
1196110610207879208	119	1
1036396766725152768	83	1
1288887726380286047	41	1
1293967478581362721	3	1
1263197835373973586	62	1
1288682868800880723	1732	6
723667743186092099	15	1
1185997330864930826	455	3
1231808609466454026	203	2
1174580128622325893	10	1
1268953888439140514	1	1
959750463589330994	28	1
984984711703195660	11	1
631302581968306218	65	1
1258729377164689428	1	1
891163518173331536	61	1
723692065183105045	15	1
1199876015745421452	37	1
654081486881947668	2	1
213412592390111233	70	1
1181403143557353522	6	1
1244086136943677552	1	1
849419730535317504	2	1
1184388705419546661	20	1
576460322190393345	8	1
723693919891751013	15	1
1283278597326372906	56	1
724629935129362502	10	1
1187313764165500939	1	1
978707094096203826	7	1
763449217066205194	1	1
1226510946051035209	2	1
1223050282804445256	1	1
1282389425535320177	6	1
1165865371744620617	2	1
1187398929327861854	5	1
1060622537731612762	2	1
150658862209433600	99	1
991540832496791693	14	1
898751047298875462	1020	4
709542695734870077	1	1
1195952321063043183	176	2
860344760236507156	13	1
942915748408475719	11	1
593546803404603402	219	2
1160251036989128795	26	1
886053458547998740	5	1
1284922928298852373	1691	6
462349847870046219	6	1
836603034473201684	272	2
969737196212981780	29	1
1278706930843652227	126	1
736756795321745502	8	1
917957745481752646	3	1
1266550413910610014	79	1
817789428461338704	11	1
1247308103997722704	63	1
1205131040453296198	1464	5
828327236574773278	329	2
1096795951471001611	277	2
1178560435939708988	204	2
1240149367231484026	1	1
1115358393813717053	23	1
761688877735215144	141	1
880544224465002516	2326	7
1209161107017703545	46	1
1239960276711899248	770	4
1189774786893729876	1	1
908198463873884240	1	1
1106021373534543922	814	4
1211428996500295822	40	1
1195978674487427175	2	1
1291994246051663913	2	1
755042663262060717	13	1
1095462826585362523	13	1
367466156803751936	9	1
1131733154420498445	1	1
526152553508110353	2	1
536010569065562142	2	1
1201731295055728660	5	1
1186577897293615164	114	1
1286522223502426154	1057	5
1064068132647489616	1	1
900220056141725696	49	1
1282634373388308481	30	1
955101569911763004	21	1
1226309717991624726	1052	5
1253382270375428158	4	1
913971287465033728	147	1
963543263447498783	25	1
289306914553331712	19	1
585284929839955970	2	1
1208324820891340821	133	1
1251221319085854808	15	1
1050789496364474448	1532	6
1169780415385587762	2732	7
1265281559859298426	842	4
1233877440917536918	182	2
1258976563265802240	1	1
1201904892491341919	89	1
1173377521396502611	127	1
297078340773216257	585	3
597136495052324874	110	1
1193438361533304872	87	1
557355558869532683	1	1
1202115978197205016	9	1
533921032562802710	1	1
1271834338073514128	10	1
785649938092654624	29	1
1232868444555317331	4468	9
1245538748469477519	170	2
365489589445591040	22	1
1068474540818186280	148	1
1279960823510601811	119	1
1197599686601756722	3	1
1132215623011815564	302	2
903022012711206973	6	1
1048395118052388904	37	1
1266548637056634972	31	1
1102053035649286224	4	1
935863490151862332	5	1
1267650218359259177	12	1
959519053607739432	2	1
942629763233759283	67	1
1258812579195781154	5	1
860433184252231691	90	1
1240787588936368150	1	1
1293578314367107082	1	1
843402484000489472	1	1
1114839212882145280	2	1
1078045640342392904	1	1
1276831060407091255	192	2
319259636811300874	2	1
1260725572972318832	1	1
979444543160205342	31	1
1044561680446803978	6	1
1279945280954826752	34	1
1058661968170471444	15	1
1247919652143890557	18	1
1191844206776438864	2	1
1060259246656204880	5	1
1171343444602540032	1	1
554485252555276316	2	1
318818311905214493	1	1
706530434665938964	19	1
1203233656026431508	6	1
1219540696298684437	3	1
1240482335514693636	5	1
1156033250117046445	50	1
1255181846493270084	8	1
1190818791152680971	17	1
499027697587060739	2	1
970323838221029446	11	1
1195309219843420204	2	1
1252384388377743414	4	1
725968569317326888	11	1
1261528192884146227	10	1
1275553040879063040	6	1
1225363895682601011	19	1
1250305414185091077	99	1
949070363273363506	2	1
1165673663740268634	1	1
1149295546163539988	1	1
1176907318483505225	2	1
1230740265124233270	81	1
706663819463753739	6	1
421464852746207242	1	1
766718043971518476	10	1
1289393357570838590	20	1
1090517472655978577	285	2
806238572033736805	1	1
1289708668304101478	13	1
1195646801269751821	4	1
1290437748028608593	2	1
1132055999453339799	198	2
1294422134763950128	1	1
1294308403191091282	1	1
603073086903812154	29	1
964332029984509963	79	1
1095135300377903134	3	1
460341395597557770	133	1
1153073998758944878	228	2
1095591192546254848	1	1
527536049216290871	21	1
1258038120243531788	3	1
1247621155699822622	1	1
942192868058087485	2	1
1198843998740164681	14	1
1141092857625718906	1	1
910997631201837066	2	1
209353536520192010	1	1
719492871585267733	20	1
855125375066701854	33	1
787212933389877248	3179	8
1161072127689105530	1066	5
1025543511229079552	6	1
1054878594553356338	14	1
1145967232271269908	1	1
1283776958018355336	1	1
1294351240372813897	1	1
1194424444161097778	1	1
993221896067895347	140	1
586556710924320778	5	1
1290117826576777276	4	1
1176026473405091850	11	1
1292092626014699601	2	1
1028573338592870400	20	1
1007449114780377148	36	1
1277458748088258571	1	1
443118262906257408	30	1
1256790025572581560	1095	5
1294125543129874484	10	1
1290718500452827151	1	1
759190622165925901	71	1
1208790965968703523	132	1
542636735331434527	1	1
282259367959724032	535	3
551277406011523083	35	1
1287298905209311272	2	1
1288659287979327602	166	2
659453265582489610	88	1
1225789905612046467	2	1
933478978595983370	2	1
1266547874649604186	1	1
1293468186003636274	14	1
1210042314861318174	183	2
1237509964403179541	4	1
1292069531380088874	2	1
1245076053047640185	7	1
1282901773962444884	104	1
1292068728686776443	2	1
309286309887868928	2	1
1225540583330943102	4	1
1282020473848467621	1	1
1193655662262091919	46	1
705261621756297257	1	1
1040902029587009636	2	1
386993194690281476	236	2
1044195488020303962	403	3
1122331013343883304	13	1
1291967394457194506	2	1
1008142985193594900	7	1
1266773783503699978	67	1
1292103774243913781	2	1
1197590470478536730	8	1
1207884092150911047	395	3
483592255169495061	1	1
1278442409126133760	39	1
1163150134092238898	71	1
1256586692488466514	10	1
1194131361808777218	16	1
1244048911161626696	1	1
717868147419644004	22	1
988301749041397760	6026	11
1102483833040949298	1	1
923102583642533949	2	1
1253416899237253195	6	1
1207120871274061906	2	1
1230485172143788122	1	1
666670728384348181	5	1
930743210450493440	45	1
1034427210892849193	1	1
1119828477496008724	1	1
1147226528502005840	2	1
1200812877217546313	3	1
886059588254826546	13	1
1105990817795018784	1	1
1199928213699317852	2	1
995116281994936401	7	1
1279462696718172200	63	1
1197561820681093245	37	1
803339983851094059	38	1
1296412438064922670	12	1
1239034341590302833	1	1
812157119373246494	49	1
903398869323366422	4	1
1017961936933093456	91	1
970475547144646716	38	1
1012662778974179339	30	1
968995158983073923	229	2
792111712366493696	12	1
1262759063729475607	47	1
1131548095134584832	9	1
1001012142104916059	168	2
1251794408337178668	1	1
949724353589813258	1	1
1268462088783659103	13	1
972449621865549855	1	1
1017492276534063144	1	1
1277299717767958530	8	1
1217311155937218603	1	1
1284970219168727092	2	1
1013988703988879470	47	1
1142993522232930436	1	1
1140106146879918090	2	1
1015044209805381693	1	1
1237570776123707482	1	1
1047681413891248188	3	1
806283465174679602	1	1
1149943241316253737	2	1
1024793136922361866	3	1
1025409536737161236	2	1
825051399158104105	1	1
1197287094477934614	16	1
1295155090105307138	3	1
1051436653274746971	2	1
1196904058968088686	1	1
1075240993412100177	12	1
1254981678724812860	1	1
1084846347074678804	3	1
1082123021977923667	1	1
1140138606267215983	114	1
818903078308413491	9	1
913168641497903185	27	1
1233630775493001219	1	1
1232182630670139482	2	1
1292007787039166484	2	1
1291965890400747524	2	1
1291751342045397053	2	1
1292271528599359538	2	1
1291930859657760973	2	1
1291161973148483644	2	1
1291772893239185452	2	1
623038662921289738	3	1
511228792920997899	4	1
1246886214783729734	3	1
1070930203557249134	1	1
1295254742225915936	1	1
1282125441184039058	4	1
391181739223023619	1	1
935142433279311932	5	1
666816887249960980	1	1
691727539235979420	1	1
1275402349896007694	218	2
1175868401088999460	1	1
1182889637694410774	8	1
922578647100039168	6	1
1173733991472443523	1	1
1126356979800080434	7	1
1229830301388243075	61	1
1279186519453859972	1	1
546823144498003986	9	1
655756196761960449	8	1
838600655845195797	2	1
740533065302147112	7	1
929503912728334407	131	1
746067461878579251	1	1
1246857021995614271	38	1
787547862594093100	7	1
834877689608405014	10	1
1085320666494021632	37	1
757640929057177751	2	1
1129308760519749652	6	1
1137584669500653618	17	1
635093189384077313	1	1
1170466469520355389	430	3
1288574387980599318	38	1
1071375121589223434	3	1
921906020475891743	1	1
1265748999428898984	4	1
1223317925465821306	7	1
954854246753370182	2	1
1016340154702626848	4	1
1104392698879819856	2	1
243632806041878528	22	1
968959499731869706	8	1
1261570185706602591	17	1
1200119011149611041	304	2
1251736693757710346	195	2
1289596370591678475	69	1
295915777335361538	2	1
1229085908620410890	9	1
1139655521721384965	1	1
804707845383127061	5	1
1253648666988642365	1	1
1133862352152956959	46	1
550389084980510735	1	1
1040642214835011698	2	1
833014933545287721	43	1
1075222921456386089	2	1
698550884657004575	3	1
648586193016979475	1	1
876524126771220532	3	1
1224806832401420390	6	1
1219393462118645801	1	1
990655580886671390	5	1
1263145275153973249	5	1
1022165483778211880	1	1
1108692208820953088	2	1
1278830690787397755	4	1
387069579282874369	3	1
1025544366221177022	1	1
708263957240086578	5	1
1242028743032311810	1	1
802882445757775892	1	1
371312539755085836	28	1
867598723752001586	2	1
909164192479711302	3	1
1209482763938562078	1	1
1274425710110310537	1	1
931291509087686656	1	1
1290472776506806293	1	1
1134407061006991470	19	1
1093263358523883611	1	1
1272666680501211180	1	1
985171050025332776	1	1
1109361870625833041	2	1
995402704891412521	8	1
511820066145435658	1	1
606060909332267008	6	1
967105302161932339	294	2
919539205112229938	1	1
1183462587187331122	2	1
1278146409140457489	1	1
1249855251931070591	8	1
1045080690888290324	32	1
937834156942057552	3	1
1149448759453962310	28	1
813040116183597127	52	1
1204522043815493683	203	2
1216657066052157514	35	1
395699311922642975	2	1
1215472620334747710	35	1
1097154420048928898	11	1
724686335750832210	4	1
661985095036436502	176	2
1277583622026825740	52	1
809476748537364540	52	1
1043272912217571388	85	1
969636480601444433	5	1
1208474842098302999	3	1
1110972251404238848	18	1
1201121059076849668	166	2
414120765324132362	24	1
420379755276271616	466	3
1295490146468237374	10	1
1145051299650482238	59	1
1158063814323994785	223	2
1273159583795384320	364	2
1272804303681224714	4	1
875646224315858974	2	1
899448914191716402	6	1
638935563705122816	303	2
217439211240947712	541	3
1144642774344421386	107	1
1239653857982812230	24	1
1082792307973165096	2171	7
566804844720029702	33	1
803133613784039424	102	1
1146447177456046223	84	1
1170783369378922527	318	2
1239766624215760907	6	1
963265648354529300	93	1
1266456626664177674	29	1
1192944866821427290	83	1
777887544380620870	108	1
628277457446764544	6	1
1134456031372644513	106	1
1259459815441432696	45	1
694504425963651144	3	1
670998000553689099	1	1
1253824451662057585	1	1
1216182001732947978	1	1
1238127359383830549	1	1
1229216985213304928	1	1
1286912173607489614	5	1
1002002816879046697	1	1
1215266051340898356	4	1
1098718047902105620	2	1
1244877939800281142	2	1
1207080363382415420	26	1
1296918397355036787	1	1
625901555216023583	1	1
689236193107378196	3	1
1039947015804682335	2	1
896836786456768512	2	1
1046316151761809408	1	1
1198716327322464478	1	1
1191048739842961448	1	1
627896244274069517	3	1
984893672506134569	11	1
663067846640795687	2	1
1000650867986411580	1	1
742266816780304515	3	1
913930459833040896	7	1
1134123919662653553	238	2
1231633604778659850	1	1
1260584165355819099	1	1
828713267441827881	5	1
1250523777151012976	1	1
1126717653046796389	1	1
555380073797255178	1	1
1177278143946563645	5	1
1062192668450500639	1	1
1271796878555484222	159	2
617459305695936553	1	1
1189633459879153777	1	1
1226364590892388435	3	1
1119920980320600185	8	1
1291113679064006766	1	1
990996831225933964	79	1
1183144713499459616	1	1
1295780118920302737	22	1
984701309301182465	1	1
1066895385190207618	4	1
218925399613243392	1	1
1160329043825139873	2	1
1150007889788944394	1	1
1233178067229474818	51	1
1161101983445422100	1	1
408747470013726741	1	1
1211825788643573794	1	1
1023987399514132523	1	1
419759032010539008	1	1
988008740718538792	4	1
1096000297190563933	3	1
1063757777681514546	49	1
960280149788594236	2	1
1159928606466785320	1	1
668398013882040330	6	1
1281753143599697923	2	1
761666520308514847	13	1
583897328834969600	3	1
843488090651754536	190	2
951932850825986108	1	1
1005733581261389865	6	1
310133656540676122	1	1
1084703603924664366	1	1
1280681455608926282	2	1
1098263337080459325	2	1
1223521366364524554	2	1
1002406937519992882	4	1
1251844865860436042	16	1
1286722465615052887	1	1
1024586930660315176	2	1
1272997087545655442	1	1
1152771520763015228	15	1
1204041694560133121	1	1
781589136133324851	1	1
748975850388455454	1	1
594412379241054228	14	1
1110963340303405106	1	1
833230738081316915	6	1
1265928437034516521	2	1
1102705281277894696	3	1
1188946525812969492	4	1
921655382705831947	1	1
1210798187237875752	1	1
1132785271839129672	1	1
1274182841227542549	1	1
1115729328844587010	1	1
1237526525977296993	3	1
1272716214388658267	1	1
1101944286720839760	1	1
615976804175314965	1	1
946132161357049897	1	1
1180280134650036247	1	1
817450121489809409	1	1
908928639926693898	5	1
1175502457518952572	2	1
997754718036176956	1	1
1145367616379179118	14	1
651467066468990997	1	1
1122937432778735807	1	1
1204173530913316884	1	1
1235645518252609567	1	1
1060643444541890631	2	1
775396650205052988	4	1
1276674818426802258	2	1
652680814043332610	2	1
328237387094163456	12	1
1164595038064496863	4	1
1299193337303007355	2	1
848626949974130698	43	1
937887962711064576	3	1
1032257763214102578	82	1
803400225833615380	29	1
452278624951992329	2	1
1243617306576158841	7	1
1126968369376149585	243	2
1281738021552652318	201	2
802463492094689290	17	1
1073363543187009667	22	1
1266543230674276362	11	1
1203387212406722702	16	1
733767392345325629	131	1
606569668936728639	14	1
1272181827812982878	302	2
664577388981518397	12	1
1276401725993123904	30	1
1226484654639550549	2877	8
433643608512528394	366	2
736016849065476187	22	1
1247761367574777907	34	1
1031258464338579607	55	1
1250887440307195987	48	1
1112287419513962536	10	1
1277631547662663806	2	1
921501644825452545	504	3
1095015244264386630	24	1
743720964277272617	10	1
335536619358650378	104	1
1233566608740454400	12	1
1294504099965829205	40	1
1071249560938233937	6	1
1192459656879161427	40	1
1257897273908531210	7	1
989701837282238486	5333	10
700550666002759710	7	1
660571834022101023	22	1
1185423230715056213	153	1
774250125299941396	9	1
1276612680978792490	306	2
1257599897839075338	25	1
1225820165963255851	207	2
915590323139395605	693	4
1258418082175651902	4	1
1259663981753143398	154	1
1297688595171115092	5	1
944284940747567187	3	1
1267191461221240832	5	1
1202759806629183488	3	1
893547557266026577	21	1
1223677739660345406	17	1
889013400934441020	7	1
1274758538438377516	5	1
472424835935633418	72	1
1254875960306700342	15	1
554099469252296744	62	1
1178232398790541363	62	1
539497372632219658	453	3
858401309581377606	17	1
772133911022534666	896	4
549804055275372544	11683	14
1149476531693957140	99	1
1090673362918985750	151	1
1142780447697403937	233	2
1248419760698298522	29	1
760156538760986665	2	1
714089567904464946	1659	6
1219472674158411886	4	1
771065479447183390	1	1
1217935500178882651	8	1
1221211679568691430	1	1
777902433786658836	2	1
1238092385045446726	2	1
873634073636110346	1	1
1096615477255602267	1	1
1172661113113022474	1	1
887489249467842631	2	1
740249483639652515	2	1
1285852789255311400	1	1
649461024029671425	2288	7
1234635819114041430	16	1
795131492194975785	2	1
1114534750896541756	1	1
1298408166429556756	2	1
802997002509090816	47	1
670839472329457664	1	1
1016860789409333339	38	1
1300516348505358398	2	1
1248704282467762237	3	1
1170276746046734369	30	1
1004124490457948201	3	1
1072598806161530920	4	1
1262707857275486209	2	1
1013714171709374494	11	1
818264044427280385	3	1
1264251765654556756	1	1
1300455215815852094	2	1
1142143769689473145	1063	5
895752155271671840	108	1
1224762586889719942	1	1
1123274881803489352	1	1
1073685338159059168	1	1
1288098603516035104	6	1
1095004152691707924	12	1
986748475423207464	1	1
1195204783624171554	1	1
1141876353264799867	1	1
687498104521752580	299	2
1055619472913875075	1	1
1212212081143844905	1	1
765011543586373653	1	1
776605676548915261	3	1
872142512607887431	13	1
1275493607465291786	6	1
1254478657003720878	4	1
834459201925152788	1	1
1178806245772247060	1	1
897186784675516416	1	1
1063913959838711999	1	1
1268605550355156993	137	1
840996628336345088	1	1
987415366294728735	45	1
1010330521127092265	13	1
1012878408016986132	4	1
739603237719507055	1	1
1118282538276896819	1	1
690606933018673182	2	1
1193726873465786460	2	1
830387000573820950	20	1
1268616677608652820	1	1
1038328667782270986	4	1
1112897873068163126	12	1
1192949525548118067	1	1
1217904517899747400	1	1
1280151162900971565	53	1
1207792663487844383	4	1
838809718310830110	5	1
1138271626488713396	1	1
1190814773022044310	1	1
1284569681897721938	1	1
1127638767533047868	131	1
1067584777194053682	28	1
1200167467683684476	1	1
917167598901293066	1	1
1243672853639991379	2	1
694311540144210011	100	1
848698536231960608	1	1
927165836215607296	1	1
1258835678699978763	28	1
703413396581777498	5	1
1083421257497853983	1	1
927736298234601573	14	1
1107122422097903657	620	3
521444065309622292	1	1
835664936407531560	1	1
350082365453893632	1	1
947561089040801873	23	1
1206330247067471943	1	1
652946190022868992	1	1
781903253431517224	1	1
1008880530848235602	2	1
1290099303473348629	1	1
806003443759841281	3	1
823327389387456614	3	1
995609846961414194	1	1
1183123246191747244	2	1
1099420115495297166	14	1
1290004339313610793	1	1
1105251425220579419	1	1
1300279155107041300	1	1
928311263132549181	1	1
1193544505945763962	1	1
1166093521099440189	1	1
1231048612633509938	1	1
1273316780982538343	1	1
1187657003997335596	1	1
1213679690875670574	1	1
854114474008117248	1	1
1119747860133593159	1	1
761423316757250080	1	1
1159952648024363058	1	1
1116133020513091624	1	1
1300173660270886972	2	1
1202012503186346054	57	1
759578139772583957	8	1
658275714940010516	2	1
1117399895389773935	7	1
1217519369576513549	64	1
1018270330546049075	4521	9
1219020551247630377	653	3
711228604704489542	4	1
1113152732396789781	13	1
915096448146743306	1	1
1278486412605526160	61	1
1281266724897034291	2	1
738568731487240202	3	1
960031325711126610	1	1
1266979223138992148	16	1
527976781051985959	230	2
1073721709003296932	51	1
1199174597505994822	69	1
1286072791325478988	1672	6
1174203224929083436	1	1
953797404526796830	2	1
1046513347165683752	10	1
975058961315282984	38	1
1125579397773135882	2006	6
1219365048309256294	6	1
757367228311011418	1	1
945780229484466277	364	2
849823767861395457	218	2
1245908733884633211	1	1
1100818646672085063	47	1
1151122705731571814	22	1
1160168515953770566	1	1
545920197933137921	5	1
845056315788230668	2	1
1054132855766269963	3	1
1000055422037799062	213	2
720314703502508154	54	1
1005935044113739818	1	1
502357166900903948	1056	5
902062795602935882	1082	5
813260675803643904	536	3
1057039016756772955	2	1
805424047663218718	18	1
764256605369532416	522	3
1259696355425910855	20	1
1189696446451155106	6	1
1250780958882398252	83	1
660213963899928588	13	1
1204154521509699588	3	1
734255632508780575	460	3
605928206918352906	978	4
994277613415714817	12	1
1109551550440947722	50	1
459167463721140226	23	1
1136313997042393258	2	1
1241866526190080095	48	1
1299422744164827199	2	1
1299422722895380480	2	1
1118756641236582553	1	1
348985473806499851	316	2
554837911753719835	1	1
1249483510272622603	315	2
1299422985748484301	2	1
1299418623638503544	2	1
775773298667683872	1	1
1055116244233228288	1	1
1299422961207476405	2	1
1299422913782349842	2	1
1178290633950101545	4	1
842912337643307069	2	1
1031975509191557190	9	1
1227731151146324008	10	1
1297718953094942792	13	1
187747524646404105	20872	18
663502315340300290	4	1
1249810093180981260	1	1
694032717125517403	23	1
650456518998884453	13	1
746672632249974864	1	1
1224827342980124706	1306	5
1280162916158410875	7	1
1267041599775571979	2	1
598125772754124823	33	1
919050259781541938	3	1
1055538750043725854	5	1
1060746419520159875	11	1
1282371478268018770	3	1
719844986211926019	1	1
1250921246913462342	34	1
1121440661464424449	2	1
1013934618325549186	1	1
783781258827268126	246	2
847087266874523718	1	1
1296580524952780953	2	1
1120430049569550478	7	1
556197649888313354	6	1
1123357752773853185	15	1
1301026142190309397	8	1
1291905746623139923	8	1
994985403293630464	14	1
1289939939856879631	5	1
1282092934195445855	8	1
1283665897692725301	7	1
1283597462074036305	7	1
1191251918442475693	6	1
1296686289437069405	19	1
1155641048417181759	8	1
1167930157059817488	288	2
1216819560406192151	7	1
815378795568693279	3	1
890506229842083880	4	1
1181545737570488371	3	1
1053644443938455552	2	1
1223850824460009562	2	1
261855568073850890	11	1
820397452867534871	7	1
737712615526236230	3	1
1267228034973438004	2	1
578444784461676564	1	1
1166852421188866049	3	1
1114077513904300123	4	1
884336914457591819	1	1
1290207063770927135	51	1
1028363906319646790	4	1
1216095697099821087	1	1
855504404769669120	2	1
1247373275319898162	2	1
1300035817405812752	1	1
1256745993215410218	50	1
1253727723030052866	1	1
1083190657788682294	24	1
1301920712302268567	1	1
1258190858763636879	74	1
1243611306557177889	2	1
1057021708818718720	1	1
1062491536941666436	1	1
1052909937552003112	2	1
909630426887376907	28	1
683816104279408708	3	1
1139311769383338084	2	1
1237512860222095502	243	2
1301644519044944018	70	1
1298757391084683347	1	1
1076909933053882388	23	1
211241426141315075	54	1
878363386918862888	506	3
669110718322442251	9	1
1108227442956582944	1	1
1252954601334771849	4	1
1234915834468503646	1	1
1291202372428632116	1	1
1300496894178361389	1	1
1261397843822903337	1	1
1119560584086700172	1	1
1301627433602252832	1	1
1002212557844643951	167	2
1291265741944914025	6	1
1072720731886071868	10	1
1296458934147743866	1	1
955860261644931133	7	1
1280925946123387093	1	1
665977953901084672	69	1
779142335879184395	367	2
351593190693797889	8	1
1090092020556648529	1	1
1199562390463840256	2	1
792678983057014824	3	1
742735457934377012	1	1
1281776697745870932	1	1
836016756207124570	29	1
1184706608840851508	4	1
1203887874433355846	3	1
678227725542096898	1	1
1109246020463886397	164	2
1238679090177769492	8	1
1025947498021408788	15	1
941231603777150976	33	1
1003664489822044284	2	1
580129987240132657	1	1
959932442578403348	1	1
1173858816396369981	13	1
890900715025862717	2	1
1277848903995228161	7	1
954472346423549993	1	1
1286073551836807261	26	1
1275128774400147500	18	1
1260967891843551257	14	1
1160907025434279976	52	1
1273415480018866227	427	3
1105303529951858758	1	1
1204875241906503722	3	1
1287376553797357568	5	1
1120689675573661747	598	3
1061576577080643705	570	3
1284601462189723698	1	1
710388301252788286	19	1
1112237335350878298	1	1
690429190398410782	97	1
968731137264467979	1	1
447799232334790674	131	1
765314603373690941	85	1
895043779344625675	8	1
1054175435937816646	3	1
1282499485536092181	188	2
1169819037627326464	55	1
1206267889376567370	9	1
599789481536651276	9	1
1264786261349236756	17	1
1297548940995989535	15	1
1207107876058046494	2	1
1046351569148448778	1	1
1154255933107613747	1	1
892085163570384907	94	1
1035163805098987590	154	1
1229934601615704125	2	1
684196199351582796	2	1
1098457076784705546	3	1
550687412351664139	14	1
1149155110337908896	2	1
794011524700176385	1	1
1232638538697146461	962	4
1052362761335738398	3	1
1190908847196475454	41	1
1199870129928945726	3	1
1136346173272232018	64	1
1250555966907220063	19	1
921201767847436300	418	3
1301765468172058626	1	1
1225646129857691732	4	1
1285550330821476393	38	1
425077336040407042	2	1
852086981784895498	5	1
1079194916334354492	1	1
1256286476551979048	191	2
119939767231053825	31	1
1291027133334032479	99	1
1274727277724434513	11	1
1292209582961328219	2	1
804930991121891379	8	1
712487051672420354	1	1
1292338257803087958	56	1
721252845092864041	1	1
444357323062902784	3	1
1064401229377191976	1	1
831513267653443645	1	1
1031236225203454012	1	1
1297598416716697692	2	1
719192833017380915	3	1
1105777826470305882	35	1
909415214611583006	5	1
1294680647172096000	1	1
1302663917847187509	9	1
888357910080524308	50	1
1139504739902558329	1	1
1296491119286288495	1	1
1295787592389759144	2	1
1006005105771950092	4	1
1268925768839467038	1	1
814657545305194557	11	1
1271182467570597901	9	1
1038546662139899944	26	1
755502160829087825	4	1
1271917331475599452	5	1
619812330968186901	2	1
1256758771309613120	7	1
1132549517850456068	1	1
\.


--
-- Data for Name: logging; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logging (guild_id, joinlogschannel, leavelogschannel, messagelogschannel, voicelogschannel) FROM stdin;
1263195476245610536	\N	\N	1277766708580450357	\N
1276302538152611972	\N	1278269981695410198	\N	\N
1075834904706826322	\N	\N	1262669820214775868	\N
1244403114447212564	1277690473800273941	1277690473800273941	1277690442556903486	1277691727196454922
1278101404141092895	1278486456704438283	1278486456704438283	1278486456704438283	1278486456704438283
1276605260110237758	1276605260609228900	1276605260609228900	1276605260609228900	1276605260609228900
1270486377460404356	1280909386369335426	1280909386369335426	1277099348483772417	1277099348483772417
1278068842119172148	1281025543181041695	1281025543181041695	\N	\N
1257987786888318987	1264273724107128864	1264273724107128864	\N	\N
1120434472114999307	1281381005474660373	1281381005474660373	1281381005474660373	1281381005474660373
1281680936316178482	1281680936647262257	1281680936647262257	1281680936647262257	1281680936647262257
1281980873041772685	1281980873629237300	1281980873629237300	1281980873629237300	1281980873629237300
1275204588894683247	1280291574131064844	1280291574131064844	1280291574131064844	1280291574131064844
1275872868114108508	1275872868366024782	1275872868366024782	1275872868366024782	1275872868366024782
1099977250817982574	1278021053322498219	\N	\N	\N
1284532619383672853	1284537814624501761	1284537814624501761	1284537675424075837	1284537675424075837
1271695303921111050	1271695305028407301	1271695305028407301	1271695305028407301	1271695305028407301
1266853535887392841	1286223869803233310	1286223869803233310	1281823992520507455	1286223755290480640
949837695050469456	1287440843707383989	1287440843707383989	1287440843707383989	1287440843707383989
1283124591048527892	1286563914817081344	1286563914817081344	1286563914817081344	1286563914817081344
1285832779216719967	\N	1285856632605118475	1285856632605118475	1285856632605118475
1260827368625279159	1289295542836527144	1289295542836527144	1289295542836527144	\N
1290472403763335220	1290818712022290494	1290818712022290494	1290818712022290494	1290818712022290494
1290787942687707157	1291118663021363210	1291118663021363210	1291118663021363210	1291118663021363210
1289647774685466654	1289849144386781184	1289849144386781184	1289849144386781184	1289849144386781184
1292985929954365472	1293149931648974878	1293149931648974878	1293149931648974878	1293149931648974878
1287589974639775744	1293756774700290069	1293756774700290069	1293756600703651880	1293756793666666558
1284193880379625482	1285012276935393281	1285012276935393281	1285012276935393281	1285012276935393281
1293699972172091523	\N	\N	1293706802206085193	\N
1294870137903517737	1294886188766855270	1294886188766855270	1294886188766855270	1294886188766855270
1292282920156794932	1292893466962952212	1292893466962952212	1292893466962952212	1292893466962952212
1151241272326099056	1295751276046585937	1295736815705395252	\N	\N
1288959741820665960	1296274737076375632	\N	1296274737076375632	\N
1295120562619945020	1295210922234871859	1295210926156550185	\N	\N
1294660772361666603	1296881142347333703	1296881142347333703	\N	\N
1297293375204229120	1297398357379256330	1297398357379256330	1297398357379256330	1297398357379256330
1275243165217062953	1275243168060932122	1298787193669685248	1298786720363446305	1298787005974708264
1277519934619910194	1300225203812569159	\N	\N	\N
1292808191226413102	1300352283619364916	1300352336207806525	1300353382443122709	1300353382443122709
1119311424473276416	1302004129073467483	1302004314214240398	1302006813461446716	1302006314318430258
1289787801973428288	1300584427273064543	\N	\N	\N
\.


--
-- Data for Name: modlogs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.modlogs (guild_id, channel_id) FROM stdin;
1183029663149334579	1252943282422550610
1244403114447212564	1286355941716922449
949837695050469456	1287440843707383989
1260827368625279159	1289295542836527144
1290472403763335220	1290818712022290494
1281274638567080018	1281275585338937528
1292985929954365472	1293149931648974878
1294870137903517737	1294886188766855270
1151241272326099056	1285061056015761418
1279472645661917347	1295883758339358764
1294660772361666603	1296881142347333703
1297293375204229120	1297398357379256330
1121045839012438027	1297673280643268759
1289787801973428288	1300584427273064543
\.


--
-- Data for Name: names; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.names (user_id, oldnames, "time") FROM stdin;
1263149952725417985	hashiketa	1724164952
1219074889147744358	slitthejareers	1724165105
1191035257080782938	.ruwined	1724166077
1233737894523310170	Prism Vanguard	1724166722
898667446246989834	cruelgrief	1724166734
1139476100108529684	war.lol	1724167191
882134033100857404	4lured	1724167214
1072503925812510761	maugatnaitlog	1724167386
1253833104875851846	goresgrl	1724167611
1241563331643445328	nigger_.1die	1724167965
718072071669678160	mikaylauh	1724168064
1252601497603149864	urgn	1724168402
1080778721507672094	Eros	1724168774
1224786904550215700	howmuchwoodcouldawoodchuckchuck	1724169263
929367172524949564	thoughtyoucared	1724169359
986128361313153114	3800rz	1724169396
692899933464035329	zenkaoss	1724169548
665950970555006976	skibidi38	1724169806
1265602796107862099	Lily 🌹	1724169900
842481817759514665	aaliyahxoxs	1724170517
1247996338625314869	bunnyrhii	1724171048
1163095472819421194	angel_princess1979._36015	1724171755
696947227289059449	protection_chen_official_desk	1724171871
974394387045949500	hachiberry	1724171953
1066908308277039214	traumafreak	1724172706
1266598746431684631	16.k.	1724172885
404015167643582474	54colors	1724173376
478891848450965515	pfyj	1724174241
1155628229646893077	jazzy0951	1724174426
733099026953666650	clubvip	1724564621
926281411927892019	pawsloll	1724174692
458916636276293633	papasbojke	1724175091
1009297782298914916	novvina	1724175282
1214595916162666557	stolenmyego	1724176800
1188490621829271656	santinegro98	1724177187
1245933709941670042	dinerofeen	1724177689
1101574819427913798	wu.uf	1724178187
781154203971616769	dictionaryofaiko	1724178541
1263433782946566227	fulton1337	1724178871
1260319864971854017	vampireskulls_	1724178889
1217060725118472285	illberightbyyourside	1724179124
1137054222047793162	muffin_72011	1724179330
1194042777428840540	t1ntt.	1724179415
1031070032937111552	mp3.moon	1724179491
1124218976998785126	m0urningstarrs.	1724564989
1266663843526873089	lastdayspent	1724180089
942698108113006602	howtoneverstopbeinsad	1724180117
998053499885584444	hurtfullness	1724180806
1191513049375457331	ratio091	1724181098
1155910485024182354	l_l_l_x_x_x	1724181749
1256196856221007893	rvyastt	1724181938
1024041233154326638	.asabestrapper.	1724181974
1160646953676329031	kurdish_gamer	1724182700
1082312546150793216	lacjann	1724182734
979301121778659338	19doll	1724182888
1154246981502386257	ahksumm	1724183492
1267880802675593246	Member Site Link	1724183731
793796627214893066	fadedgrl	1724586505
1173238864048046094	x.kiwi_the_fruit.x	1724183967
1198721656361849002	hard4saurae	1724185290
1242725270683652179	.prettyfeenn	1724590613
1264220620724506654	7ringszzz	1724186035
854751896861147146	michaeljoseph_jackson	1724186200
965747967912976394	unicornsarelife	1724186518
1208923344812900385	mademyexit	1724186696
1245616665421414427	zachistop4	1724186870
1166105482629480461	manmannmsnanan	1724356091
1191110888430776351	floringeana	1724187284
1238209866095398952	freakydenn	1724187441
1115116848325873704	red.fr_	1724187477
1212074344512094219	clzcm	1724187654
1005152479983456340	diddycord	1724187905
1152005409662582977	mwanlpulated.	1724188284
1235133342467227689	.shesoslime	1724366849
1245209973546287115	makaylaa_.s	1724188734
1027490065615704074	goretrance999	1724188865
1195576667553398897	pnytail	1724189359
1097283834283819158	xoalainaa	1724190099
1255598661857972397	yslqueen.	1724190185
1246680506309939241	littlpwncessa	1724190189
456670260351729665	conserveyou	1724190405
826134036284047440	.kit_katt.	1724191048
885038581830254633	saialol	1724191316
1270805982808637511	nannosfav	1724191428
1243029382294143006	foreverrrrrrrrrrrr	1724191855
1218189701307957380	.tatiwasnotavaliable	1724191974
874334949526863913	devsboosts	1724192454
1206778100873035786	slimwaistmodelface	1724192492
1134238281224167616	16strangekidsrunning	1724192552
1133141505373130772	elenashorty	1724192793
347108380525068308	hamdulillah_	1724192836
1013714171709374494	chpqt	1724192992
662393646418624522	herjournal	1724193247
982932498835202068	.liam.xxxx	1724193319
897817372214304850	pom_dek_de_na	1724595293
1091592488071991356	swagzedb	1724194068
1131821357081047130	gunshighs	1724194373
1157817456467906632	vauiti	1724194400
1129909379039252550	nennnnnnnnnnnnnnnnnnnnnnnnnnnnn	1724195067
1061206484798677043	layy2cute	1724195626
1233216135319650396	xlfmcord	1724195833
1159577649761501275	intrstljr	1724195987
1072907765296676914	ghwostinggir.	1724196526
1208289984205955144	naruzin_bait	1724196559
1209900703976521748	blowwwsama	1724196774
1186054672662941777	louislebourbon	1724196881
1187733081579343954	7exdd	1724197540
793006810293731358	alr.zero	1724197724
852091438628208650	iheartosiris	1724197810
1142184821200781413	ohdarien	1724198253
907015881731739728	ellie._3812	1724198462
693921990284935270	thoughtsfromourpastjr	1724198586
1104874081867796550	skibidiwish	1724198608
1163631410842710148	dimewyatt	1724198715
1254567215835910227	reminincsing	1724198982
1192180659880480901	xyhijn	1724199211
1011875213216055326	zlammed	1724199227
1034964142819377152	sextier	1724599791
943737064539697222	probablydr3w	1724199371
1261539073286471720	kikoxmia	1724199525
815666439695368224	luvqueenmimi	1724200347
917169006404829306	unseeingevil	1724200393
735269972724547605	selfsensational	1724200777
1170329565168676941	nopotentials	1724200848
1217813294983942145	zizizaza._	1724201665
1232935150728380461	_sexccbarbb_	1724201821
979514062016741456	zahwrii	1724202184
1235412710867468321	wuu.f	1724202693
899301172534456360	exlurk	1724202756
1225561540900683916	nova.rs	1724202922
924906974037020713	slimeshoe._.	1724203004
1040012520355807252	.bqners	1724203251
876219178292510771	sreapfr	1724203264
1218871038377725976	inadreamjr	1724204238
1248907843797782721	.qtiza	1724204305
844360125166387240	sykuas	1724204609
805286639278096394	davis933	1724204617
927066342480297984	lifeismyworseproblem.	1724205319
997499535012155482	genjidex5955	1724205482
734512545850982511	drugdoll	1724205630
1107099551816499200	bluddypawsali	1724205775
1251165439552389152	cravehertouch.	1724206019
1145664855802646569	pfayee	1724206236
1262062113518522529	mello.yellow.	1724206544
1228216192720961617	imjustastired	1724206593
1253712300326649948	sigma075866	1724206878
601789129692413964	slientcarti	1724207069
1071029292697391184	femdollsuki	1724207118
1130632916062449825	culfsin	1724207544
1204092116675076106	0x008b	1724208169
848153306522189875	bapesia	1724208341
956725448467939369	s084721	1724208732
860307561789259787	vda3	1724355370
1243065995258757132	lusttxd	1724208853
1121944985164599326	sillykittiyvaexd	1724209023
1168064020192964648	privatentry	1724209207
1058248537281925180	alyzq	1724209503
789373921840332821	recussionss	1724209910
923251803418660906	10staar.	1724210074
764150333857071144	wi8eaowe	1724210983
1228948640815382559	sallylovesjay	1724211286
1119357084199309386	sparedsoul.	1724211352
1204231466221834284	hopsintv	1724211537
1042091458901053470	deleteduser25367994312890	1724211987
1137886345956704277	titfatatt	1724212291
1257616288050581505	hoesdr	1724212803
1134665735608741980	w_rried.	1724212890
1167667576042696788	kissmytearsml	1724213066
823713683082313728	soldpercs	1724213350
1065029303303155823	vkz9_vx	1724213889
1148474591455486032	dollyliaa	1724214060
803243108389224458	cuwred	1724215046
817436009032581160	tracyyy33	1724557693
333305759708348416	v9rst	1724215584
639663614541824021	.isolated	1724215895
1075049858420965397	masochwist	1724216884
1198382740953903154	ribbuhn	1724217947
1172355422938730538	foxicub	1724218268
1152121795298738236	blwadegrl	1724218330
1182180048267120651	bllendertoya	1724218453
838950502251233300	attracthislove	1724218664
818123357551460382	swtted73	1724218762
797305714175115277	reddude.com	1724565660
822317962714284084	sickenedgrl	1724219041
1097439509131563138	evos_h4cker	1724219174
1132552124253868123	manuueehhh	1724219221
1033416791571050517	omgkuyo	1724219640
1034566773082697759	hermosawrld	1724220106
846938129264148580	medicineabuse	1724220396
1189416509177610312	janjeeekeee	1724220861
1101701947200905288	sorry6346	1724221675
993715681348563015	deathcwrsd	1724222005
560171334680838146	7glf	1724367028
1197941116700471306	forgettingthepast	1724222475
1058274123240964237	danyethestronge	1724222493
1238445020944662661	deportedonline	1724222621
955682233686048769	piercedgrlll	1724223146
1126785761140822037	someguywithathickdick	1724224033
1131300822051995768	000prayer	1724226182
934797717161541662	nathanstolemyheart	1724226704
1051998991920935012	novulentgirl	1724227263
1218749810614730804	140a.	1724227460
1002994105242095766	lai54	1724228120
966815375306149958	qtmh	1724229289
1166981359424786443	_hauntingdreams	1724229292
713128996287807600	futcheliosi	1724229999
695618472880635954	fadisfangirl	1724230431
1271112140287115399	hacker229229	1724230526
1188975958011674745	kharz0613	1724230739
1189270911463993448	agirlsemptyworld	1724230915
298435309178191873	vinny.py	1724231066
842901903704457247	cntfindmira	1724231194
888369150630694932	d_spire	1724231602
1240469605600723024	xyzqiv	1724231744
859087110757416970	12hoon	1724232780
971466983927324802	alexxprime	1724232826
634511185735319563	dark2_0	1724232835
1196033797272117261	thighsgf.	1724232876
1146427714266472549	otonableue	1724573938
847415751753072670	cashmoneybands.	1724233043
735428417134133259	evyveraa	1724581233
1160773145054150677	aloneinthiscastle	1724233597
822140447258443808	khalid2085	1724234529
1174839428334764073	makedischoppadance	1724368580
1071844186950746155	1nonly_korencek	1724357991
1247724474128928823	giaissra	1724357992
756627843991208056	demsy511	1724235184
879960724061970443	mayalolxdd	1724370356
695886185901457408	jennifer.exe	1724235710
1201228620211957850	anushkafr	1724236559
873198849924153415	jijimon.exe	1724236571
1190396084611203124	bwunniezs	1724370918
1251592362581426257	PetsLink	1724586881
1221260353841664000	ohm1so	1724237090
731312838085181470	katvieyesh	1724237227
1044309105491329076	w3b.alex	1724237271
1005246130382188606	vexxedinthedepths	1724237324
1259228294381830175	allstardeja	1724373825
1231071772481421423	popstar.boy	1724373830
1228487294290497566	sky_01000987919	1724238022
1160523484812820543	deleteduser45689	1724238819
1138505512309239858	sexmanic	1724239406
786299411293667348	T1⚜Gleen	1724239522
872101474929373206	tankdelupta.	1724240109
541005385838886938	dolo4s	1724375482
1275075996491710474	jshanakim	1724376913
772943697082843206	cutiprincess	1724241220
1255610941962190932	mercyyv	1724241269
1229972124001894412	andwhenhesfoundhesbyhimself	1724379721
1195248954523258981	fein4_wrxdie	1724241603
783786847150538793	dollwgutss.	1724241631
977638278612287558	cigsgirl.	1724241664
1224920635139166339	lovxkxnny	1724381391
1224603514785759272	cutstain	1724241795
852814594048524288	lilnutnuttmrtakeyosoulwitgen5	1724242154
1055263229665886278	upinmyprada	1724242237
872483147932114995	kquf	1724242548
1208539499286765570	fatpiggy2010	1724243265
1213891074683310204	smoked6	1724243858
1237466122408689845	melly.belly0452	1724243924
881665343834173440	oki937	1724360494
1133128949174648934	debatefunds	1724244156
1215104254851682325	sendscreens	1724244251
1144530323057684632	cwult	1724244549
1248903720763129941	debutant	1724245281
1058682881960067112	thismynation.	1724383260
1238939628590075974	patel_143	1724245619
1087104965807452170	habitualsex	1724385429
1086401239891312683	puccagarukiss	1724246298
613176557015662640	qtgu	1724246572
1159289734003183697	arpoq	1724385719
849753850813612043	cream444jasmine	1724246766
1026345085543137320	xovg	1724247130
1185843261676466176	karxmsx	1724596411
995256741048623106	kaydensimper	1724247825
1217147040589676606	11111111111111101	1724248083
1261370535997210706	arisbliss	1724248196
1229081728799477832	code_morse	1724248444
834421264180576267	gonrqqzz2	1724249732
950183297839955989	praeoni	1724250505
1267440086673522691	walkedout	1724251796
898393688470855731	vsxsp	1724252107
836016587713937440	koreski	1724596435
1133809042263920751	fluffythug20	1724252261
1208108647037796404	uwwya	1724252273
1100957738445574154	_ilovestar	1724252382
1265857812035276853	bcqn	1724252662
1120336052780015687	x6nny.	1724253340
940768852231483432	friends79	1724253845
896211724552781865	rotinmyarms	1724253891
1012903030653460491	daicoconut	1724253903
1211385828324941945	comboykiller	1724254500
895792076690702396	stat_.	1724254730
1241816141513494628	/・MultixBot	1724255161
1163553736380137563	eddin_lostinikea	1724255343
958141336945586176	.kage2k.	1724255392
787615294108598312	lucilas1	1724255723
1252678324820643877	27_xspr	1724256002
700925522263277651	jumpypink	1724256316
695801020269461562	notnameask	1724565691
992796692543979621	bodysplit	1724256435
1216947543146238013	trustpape	1724256709
535635352799412224	lil_cab	1724257012
1111158357877862400	Galactic	1724257029
1230319627297493112	chocokitkatt	1724257193
1246478806827536495	bubble.c0m	1724257710
1249479470386249761	k4cn	1724258223
759107400954806292	logannk.amouree	1724258316
1089143453948059650	puccipuccipuccipucci	1724258954
1248090558640033884	swishcheesethatnigga	1724259136
769012702357487626	vmnpire	1724259201
1095825476892774490	remedy.lat	1724259279
1014093357867356190	user1014093357867356190	1724259456
1146001332675809320	criminalfelonies	1724260044
1176243383342219386	vrtualwaifu3	1724260167
1008454866068324503	rresiduals	1724260466
1275532802707689584	apbg_oficial2	1724260594
1159817546132889610	vtyro	1724261064
1225932667493552279	FiveShield	1724261798
1184356761445089372	herpussylikewonderland	1724262256
1138269617152852059	yerkoset	1724262538
1248338344325414995	narcotizing	1724262849
1158639100891500605	pandagfie	1724262959
657778342216466442	lurwed	1724263358
606406224879157259	dayinthelifeofayoungbbc	1724263426
1180418166703280128	asvxnz	1724574426
1221980037352263681	vrslu_tz	1724581862
937077853718183947	extortionates	1724264825
478144606622711808	adorbsl	1724264927
1236121105370976297	awetots	1724587153
1022956141719859261	rvssviiqw	1724265262
1122672822943232001	leitinho_92002_	1724265440
1215084564939014214	m6niac	1724265854
1244806395644215333	remurial	1724266029
1249162668221141032	euylin	1724266036
1182828090091655243	kekemamas	1724266162
1212394665681231893	getoutmyhead	1724266313
1123866260892024893	adorwie	1724266406
867673944831164426	yzqm	1724266726
1225478153753989176	latinodan	1724266737
1252063603683758107	riaex	1724266811
1232590868339232781	bd6t	1724587399
1048418117224779837	Toronto	1724588788
754366867254018119	duepast	1724267030
1269942643954028575	unlashing	1724267191
503082878763008000	vxcmpli	1724268084
1191678544284221473	onlymeobv	1724268175
827929172726513696	bliss.xd	1724268266
1145210703930740868	Trustly	1724268347
743273704338882641	xxemosuperboyxx	1724268404
1257016326728192051	allyallcansuckadick	1724596885
788799817908092978	Zorojuro	1724268993
1118285011746029598	oneyism	1724269272
965607891258212402	d9stroy.	1724269357
992959631137710100	5817234	1724269719
1263019574127890456	traces2khra	1724269837
1192599700445077517	florqria	1724269941
1061512064306270239	.getoffthatdonjulio.	1724270149
1060443864797827103	maiwaixo	1724270695
1132058860052545566	e9hd	1724270710
761977306499121180	22.38	1724270896
1049367805402816532	Akery	1724357865
991545047025729617	prttypunkk	1724271363
1260733782613430453	boostiosupp	1724271377
1236585942098247683	crucifyherwrist	1724271688
1129838460514087002	0o0o0o0o0oo0o0o0o0o0o0o	1724271718
1249656803591979064	ukkut	1724271898
1128388396826509312	fatherpeaked	1724271948
1215379347309862946	wildinz.	1724358092
1213557102581387338	.flyynyshemaa	1724272074
1133616216733388911	camyrnnnnnn	1724272129
1179522983597973649	cutmywirst	1724272281
1128646851525087252	h1wzy	1724272586
1090292246676516986	brixdolxdol	1724273277
1068260917327970324	xsprtn	1724273829
1124010970222702692	5wjq	1724273869
1254647357975564322	fromnez	1724273885
730698219968790549	sn1tchez	1724273936
924718741005160498	hadeswqsfuckingtaken	1724600016
1266977779040260097	.seresubii	1724274327
1069405577991700570	ohio_nerd	1724274395
1200886643968725144	mowgliq	1724601979
1160272259005550633	19rot	1724274418
326720789569339395	i_cant_feel_a_thing	1724274978
995754523807186945	2insp	1724275362
1055558177304887357	.iknowalexias.secret.	1724275421
1135674947855978582	remainsofher	1724275820
1242545908239831042	debations	1724275827
1213969093527470130	4monthsx	1724275964
989193221349474325	newpints	1724276219
1170746262539214859	nirvanoid	1724277026
1224149538223296596	plrbltzd	1724277050
1061582555545088070	ekitti.	1724277616
1205860868672458804	remuriao	1724277761
1027236281975050310	fks4	1724277793
1222262517846376500	kaiiivxy	1724277895
635337166733574175	kissingyouu	1724277955
866956838418251807	ryonbbb	1724605908
890938645224230923	indecention	1724359501
1224544655866073169	nekuwmi	1724278347
1121962281715126302	alexitap	1724279178
978744492729454592	reverings	1724279223
1061627681080348702	fwhbyzj	1724360134
1246538974969987215	tiredgl	1724370601
1121666456057299005	haki_dev	1724279320
1155227035367653567	servinslat	1724279739
1212520491756290102	jaydesfan1	1724279969
1092281673799962624	raginghotlesbianporn	1724280391
1205251687053524993	rosemary_heart	1724280588
1105029048264044565	kw1ttys	1724280824
1201514315447025686	readingher	1724281287
1104532891435806780	alexrunu	1724281727
141389986766389248	healingdemons	1724282313
1228204891646984232	nonnononononoonononnnnononno	1724282785
1208634581750648845	stqbbing	1724282786
1136494248317956107	diaryofher	1724282862
1144448142088097883	banging4kt	1724283041
879477958702661694	comhurt	1724283130
630314786717958166	killingminors	1724283155
970876818334830703	taylorportjunkiie	1724283224
1267637457206116508	recensies	1724283245
844903425316487209	cutietaiki	1724283841
1130676525230989405	stellasfav	1724283965
1132884086525005934	interlude_.	1724284060
1210085547834605599	somefuckshit	1724284205
1079684045753036890	334xviperxlix	1724284599
1010559477138862120	revediaries	1724285349
1269953538575044702	dcsiredlove	1724285447
1171963014241595404	puppyydoll	1724285530
997702906314772520	6924613	1724285573
1193885387794423872	8rinn	1724355439
1034479258422231141	16c6	1724286104
821420673112866847	ttmagain	1724558071
1023908838996455485	teenslat	1724286478
1102582118263029860	aiiw9wowooaoa	1724286625
716715241844768869	vilatina	1724287524
1126621114051866654	fuckwuu	1724288023
1259598689052393568	slitoncam.	1724288237
945800721540984962	kgdifferent	1724289071
759205214741069855	rangersoull	1724289545
872283312457125898	fangsinmyneck	1724289714
1140482923733196850	xw4v	1724290008
966372897927073914	dollcraze	1724290148
1141323818879680532	.admiral_.	1724290148
763915914990321705	s_ftly	1724290741
1160058609254809663	seungdz	1724290786
755620348493430804	04101124	1724291224
1095516537659601100	supawawg	1724291230
1067254727252922439	gruesume.	1724292200
604036091766505472	w7rst	1724292305
1234332861876670487	purechocollate	1724292622
1090882748987748414	.tinypawfie	1724365124
833638140236398592	noobeelorder	1724292961
678140573869277195	lixw._	1724566062
1207520683194585089	killdeath_999	1724293390
1136417362690703420	ariaaannmnaa	1724293535
1111116985422581760	yslslimex	1724293733
1033660602293440512	iamhisvirginsuicide	1724294296
886840252646453258	untexpro1	1724294657
1122324879270752326	b6eg	1724294692
813457731692134431	textmewhenursober	1724295520
1189475137326690387	wylooswhore	1724295827
1125204614296387665	fuckniggaskyssss	1724295970
816473021291692082	lovemewhileimhere	1724296043
895727999532548146	miss.puffpuffpass	1724296189
1197436286601015317	wockfeed	1724357236
1254097067484119183	icepsycho	1724296407
965398241732616202	bliss.medic	1724296613
644710205992468481	kalyptra	1724296905
1096551749424267325	ghostinyou	1724297062
1127332448670335049	bladekink.	1724297299
1269558472358494220	phamtrannhatnam	1724297420
1015327403658182657	makehersh	1724570893
1222111370284109886	00000001010101010010101	1724366911
986578917274038282	onacode	1724298901
998443539769864363	takeawaymysoul.	1724299640
969640133634715708	vv7fijdsgvu8deyf78erffgeriuvg3ry	1724300076
1203110280528273508	ih0h	1724300157
764225335154966538	bllaahh	1724300399
1142312386070585344	analysic	1724300840
1251215526709956643	rvlkxz	1724367843
1147040934052245504	rockoutdev_	1724301907
1210412651025408052	warclips	1724301943
1175268530250330222	bloodinhdhdgshssbloodoutgsbsbs	1724301949
1252293308169064607	.pwretties	1724301980
1247018928270606452	2dkills	1724302035
891744794735435826	me1ow.com	1724302205
1077446610243563532	dwlovely	1724302206
1142071863808364544	nyaichinisannyaarigatooo00	1724302543
759901058943418388	isolate2473	1724302933
1242588876758057031	itswhonae	1724303088
1242882971141144617	hiiiminaaa	1724303541
932026596334919760	crimxk	1724305007
969950946606088232	haterrrez	1724305162
1210553529194778645	dollphny	1724358038
1048244583978500106	gj2.	1724306438
793107928558862336	fleshgash	1724307622
1115292531220041939	averly114	1724307942
1151622028500156467	fantasizings.	1724308441
1213672939128365099	gutsnngalore	1724308524
1010702535088144394	very_fluffy	1724308925
1115817585884282952	iuaydtyuagfad	1724571097
1115775453043630080	vxmpir3bl00d	1724309981
1193401573678776351	chinesebitchh	1724310042
1153103316113440858	llimerence_	1724310291
1230890652041216110	Zero	1724310327
255841984470712330	satom05361	1724310386
1258320383116050507	rottingwrists	1724368403
1239014933409169500	fuckoc	1724310971
1260391001554419764	r9th	1724311119
1221930833854595172	DuckAI	1724311370
1086362837011677346	vivianadarealest	1724369773
982249977420054558	mycoolusernamexp	1724312803
777623766410723328	misshisgrave	1724313966
1224181187514339410	hangities	1724314007
1175210918695673968	capturable	1724314519
1203225045669773373	deleteduser13848183	1724575093
1127678137887621141	eepy.misa	1724315916
1241089525829079121	d6mii	1724317337
1247753056544882788	antislamic	1724318742
940815741559664641	kcartz	1724318772
1140804742197547018	.noluvbuki.	1724319279
1111832927177805894	serameera_24412	1724582376
878254881335545856	leo_chexxx	1724588216
1074044255372320888	idolalice	1724319955
1273590364522942464	PatchLOL	1724320286
599703897971490846	only_and_lonely	1724320408
1191791835169951906	zpvl	1724320580
1119590260108705822	brokecondouploader	1724320785
1259208528099282987	4xnzi	1724375558
926083232200531969	bsbubyvssuiddslsllsksududi	1724359833
896665725366829057	zombeegore	1724322027
1134294018914791424	slityourneckforme	1724322216
750379503179661444	coffin.py	1724360148
1221086621152055318	thunderlegendyt	1724322932
1090507881469722715	igorpaugrande1111	1724360199
1270020348170997813	shortcake273	1724323336
1055046422753460294	ak47user232	1724323632
949498197011746816	vees.toe.fungus	1724323814
967968565049311282	urdyingdesire	1724324394
1021534154082496533	lostthoughtss	1724325423
1221835402009247855	freakzzzs	1724325558
1202300162794606657	8723687956789867156787689	1724326498
1232478797228675198	avoideu	1724326688
1144940400625340416	iimoontaeil	1724326952
1186004787293069342	chlawing.	1724377128
670742806373072918	fisheesz	1724379842
1137863998021308558	jheneaikohealedme	1724383587
1257762261074841771	kayanaa_off	1724328342
1257810772214419467	slimedphat.	1724328760
1272533198932279421	54321678xc	1724329226
961016602944483459	crazzyy.zzz	1724329445
444224755533348873	midwestpenpals	1724330433
693528527219327118	8luurs	1724330570
992125489852469278	djolethegoat	1724331985
1195530211224211568	killaking0819	1724385894
1040627347084300288	gl0balziyad	1724332171
982285384773947393	iwanthimtofingermypussy	1724332233
1049851258623758406	xiaaluvs.money.	1724388385
1183573204023902208	Clippy	1724333259
948549945198252032	mmourirrrrrrrrrrrrrrrrrrrrrrrrrr	1724333886
609500542456037400	jung.wheein	1724334253
1198146857935831122	uaoif	1724334570
1131379091933765783	98o89	1724334710
1155540218309517363	duong.204	1724335073
1155724248988536882	squirtforkye	1724335429
1261335155864371312	0v3rdxsedd	1724335531
1273962667710742664	melmeltrixyyy	1724336041
1152972900505235586	blehxdxdxdninilol	1724336653
1006365104754937907	.villain99	1724336704
1131742823826325544	darking4565	1724336713
1129870748215939082	nadii_i	1724336940
1037663936952156201	4clovrs	1724337009
1108441095832080395	holdmedearly	1724337541
1236442003286523986	6fts.	1724562700
954191659208413195	kosya.nya	1724338155
1198128496174714973	fishhieey	1724338681
1165694625688866868	sogonee	1724338876
891958035629637673	iamnoticon	1724339226
935639254460170290	cutesanriogirl528	1724339234
1095169265310633995	dcllygrl	1724340284
1249932274422513739	ratedky	1724340439
1098059847548817478	photosint	1724340660
767030902961209364	sunnyisbetter	1724341126
1272525403562578002	userlovesher	1724341543
1082458640134459392	cheshengg	1724356366
1273059341238272001	morgueshewrote	1724341922
1092938976886800488	xxrtp	1724342073
1210084074614427700	lcial.ii	1724563009
988823523067826206	sex1nthecity	1724342279
1223753151333793924	erixxca	1724342644
1258876804727439431	st9tus	1724343142
826335327366021160	fw_saaz	1724343332
1244916833966882829	exe.sg	1724343887
989760579155689502	ng_absolutedumbass	1724344254
1213562453938544700	v_liamcc	1724344400
1275269198343569420	y.zke	1724345093
1264972256837243003	isabel020268	1724345315
1249885334632661066	_yaelokre.luver_	1724345385
993904651399340112	xnlm	1724345496
1159632158554603530	.diaryyyoflay	1724346180
1272611588376891518	himatest_	1724346306
850736390735527966	fraudyuta	1724346831
1012817694329933945	ruinedmikka	1724566695
1257151961673760768	wally.tx	1724347194
1127080876229017650	dskii._	1724571291
1269038836852457523	unstabs	1724347408
1226521480850837645	helikesmyfame	1724347413
1066336637489004655	d3dndh3ven	1724347808
1253351619995766836	shrlinee	1724347902
1067513249068765195	sdw7x	1724348242
1171270512417189938	allmyfriendsrdead	1724348310
977240220414120026	SCDC GlobalChat	1724348371
994466053046415420	zzzzzxxxxzz	1724349429
825713535044026380	freakyd0rk.	1724349499
846497554190696448	x6up	1724349674
1184946795973988463	molestedher	1724575169
1176217533515300964	nottoofuckingmuch.	1724357753
909133464874397706	msscapalott	1724350234
974575793793531924	phetsie	1724350710
1166348272798023701	theconartiste	1724350975
1244065624909418586	prettygirlstop	1724351159
1229176916246925334	teebabyyy._	1724351303
1254582492225343502	dr_inking	1724351415
348993325828800535	0kokok0kokok	1724351877
1225265807903428721	madthurll	1724584473
1240170825106198578	anti292	1724357882
796527333833048085	mioxoxo.	1724371149
1150059005427863582	givemeurbankinformation	1724351910
1207886156340142102	jirwai	1724372876
1250007342175748176	xander.co	1724352864
1152687597957693480	imapedofile22	1724374696
753477130289152121	ms33k	1724375952
1115360872194375770	wvxq	1724377697
1270147608689643640	kzdcsz2	1724379894
1225009615281061904	girlfans	1724381581
870382032159670282	mwelaniee	1724383722
966152723730923601	p0isonb1ood	1724359850
313400532528267265	tufftony6	1724386134
1181413047634493453	scramlist	1724360305
972153806945148948	ruinkurta	1724353290
1150504018951540847	cwunts	1724391797
1179434447091810307	sexnhim	1724360807
926333853784739891	m.eiii	1724600057
1028281281236181043	moneyjusyaneed	1724603268
1182357579918221403	cutecatkitty738	1724353616
1123966846618579025	sexman3217	1724400626
1239292324199137410	maltesische	1724361147
1016528508807294996	witchevening	1724361227
1259491406519734323	extortcomsluts	1724361490
816230752601243658	xvus	1724400690
1150056771956772965	jenny_hallw	1724403323
967049785804726302	605x	1724603488
1114795067354382388	pnkrange	1724411439
1247575731291033681	ruinviens	1724361711
1156545844321988648	asiangirlss	1724354195
1217620169510359111	chingchang0485	1724362260
1091478754368442399	emptysoulssss	1724414107
1193401385828499478	.hisonlydesire	1724415758
915127707073925172	bazarum	1724421614
1136311196715335680	8japn	1724423121
1260815386656636930	slimestfreak.	1724424730
911283138943123477	zzx.01	1724354885
501905225360211968	222html	1724426530
875941926757601372	evilbladeesdaughter	1724428009
1075624329888403536	truffy.028	1724429238
734733906712199219	winnerfish1254	1724430510
1014900235492933632	kayasora	1724432572
1153379368308068352	kit4yspaw	1724433276
968572501401698384	skamfoo	1724605947
994668236589252719	Zero Two	1724436502
1172567343415697539	kleben_m1	1724436679
1251671696268853299	Tonnai	1724440057
732683504948609115	xskri	1724363542
686535877182226433	nicolatest	1724363586
1041319070970171443	v9982	1724363630
1047123618599010365	cutehkgirllol	1724363695
1250157360224272386	1_.om	1724441172
1237087452385120337	hilolokbye	1724607767
1235670562681126964	holdamansnut	1724444979
1115772768101863494	wickemnae	1724447299
1207696179383631882	zenaxi	1724447871
1120499282722697257	aerivsae	1724450755
1111288431448957098	pizzafart1087	1724452654
829855042819457074	war.hymn	1724454160
969979778218213456	egosicc	1724455434
873760053923020853	drako_arc	1724456961
711229345439416484	roxcks_	1724460034
1180734479606743050	flexjugg	1724461160
1188647729866489929	nuksake	1724462860
1207080228179021885	VS-ASSISTANT	1724464077
1253538367392448535	agsjn	1724465658
1214397915498414112	chriseann	1724466905
1082712837371203666	finalbl0ww	1724468974
1191169271150166098	glockinmyrariiii	1724470339
894739473114484786	irlcatboyyy	1724473270
1104562032818266123	._omicron_.	1724480188
967322553825775626	sshakjd	1724482482
838865442197209099	ilylain	1724485346
685117463029088256	aimabiet.	1724486064
1161506316704038962	4zcb	1724558348
1137519981987377234	gothicsoulist	1724566751
738449588637139074	daisdaughter	1724572260
1099531211770187829	icufae	1724576219
1146232905429958746	dickfinder	1724583270
1228656005450301471	sold_acc_202059205290	1724588881
1171911269423513640	bitchimlaughing	1724593273
1087083746450231418	airprovrrr	1724598502
612552590906884106	arbitrationisfake	1724600671
1081048686915768381	tokyosweetheart	1724603636
801590839042244639	bloodnlimbs	1724368515
725556358111559680	phmsgf	1724606360
1220578555092668576	louaf	1724373306
1146488693373284524	mymommaraisedabackdoor	1724374737
1217613515653910529	netsight	1724374903
1155229746624471061	loldejavu	1724375200
803570237525590036	igga8194	1724375955
694943789730758696	5hxn	1724378034
1197315520396021842	.whydidyouleaveme	1724381148
1143258507349598360	.kittyyyykattyyyy	1724381610
973371784806137866	shokkusuta	1724384621
1241859449157718020	onlytravvy	1724385411
1050937798598860870	bsxdlay	1724386427
1180837015248445512	crownedxx	1724389869
660965944931385344	xariyana.	1724390285
1257853650739396751	9erski	1724391415
978087062303551548	camryn.2real	1724607923
1005960549655388220	dtbzen	1724393618
1260267406979239978	thatguyjoot	1724397518
980734798622502962	moniiii8650	1724397629
807952347228536883	szakissed	1724398177
1252597629725184095	soulsold.	1724398756
1198367382608019627	storm_1.1_79022	1724401998
371001892060528641	tallrichhispanic	1724608770
1024291425258578070	suaontic	1724404579
866609524009861120	aquamarine_07.	1724408996
919712012123144202	abused0001	1724412242
1142393919615799336	xj7von	1724414845
1000117081158717530	gorehissoul	1724418496
1217113305949278449	hertorture	1724418696
651061337992200192	cursed59	1724421750
1094920571357253643	dj_ln3	1724423790
836154869265465365	erotizing	1724426917
678593629266116649	richandalone	1724427287
1273825426451599424	2twicelippy	1724428110
1238117626601799700	maxxxxxine.	1724429308
1197299604249645126	letssufferogetherahki	1724431041
1007366549042118776	xavier_loves	1724432899
1123052176034500739	user8271639408xyzyai	1724435631
998400705809367200	j9et	1724438421
1153467197700706315	aiden.st7	1724440184
1219378469876666468	lacedhislove	1724441456
1202408190487175171	simbible	1724443694
1179942065862353040	seducida.	1724445284
1201495458044973126	yourafein	1724447324
754823354011353161	girlwhoyearned	1724449614
1173227781866397807	suicidolls	1724451149
321529369426264069	gunnjng	1724453029
1244979445077643378	fx.ltc	1724454368
1235718678159429652	xusernemee	1724455929
757563835048656957	wpzt	1724456983
1092915915068289186	ashhqzl	1724460580
1112784469376634931	fallendall	1724462472
833053389826818118	luhvrnaii	1724463308
1262943338340945920	abcdfj	1724464985
1134477704943648768	xdxdxdxdxdxdlololol	1724465784
1247184438522286234	endofwyou	1724467942
1124250776341057536	deffnotb4nny.l	1724469236
991101370142822573	2dfraudd	1724470748
1180357346522837062	atlxtaboykarii.	1724478224
1237389515446947840	zackk0640	1724478808
756430431997657139	laviisan	1724480334
805084603357724714	_alstroemeria__	1724482851
1270864589654986856	325 Bot	1724486156
920542729124057170	tfwvegito_blue	1724486782
1134619686487740426	laddysherry	1724489533
874940742278193183	hazzzm10	1724491463
1238603796737818744	wifemeupp	1724493236
1141416611417444372	26dahlia	1724495648
806233234925027348	bloodstainedshirt.	1724497615
872264292697800724	conflagrations.	1724499682
443833184736641024	saeko.vendet	1724500751
1057460472464543754	bloodytayski	1724500933
924323601920978965	casycas	1724502081
1086729480384548955	b1tches_fake	1724502498
1153647563724034058	xtspy	1724503234
1223543868448837652	jamessmith0088	1724506010
724919137347960873	mightbekeir	1724507679
647507149424951307	.burger.ye	1724509183
1207108702126219344	replacedyou	1724510001
1211000923149570111	strangerss_21	1724511056
1008800480933187665	ghaymarfrfr	1724513412
1256371614107570186	0jwu	1724514698
959184871966797885	kyuetana	1724514780
1181199249233416286	darknessofnight89	1724516856
771284817652350997	reuwitha2	1724517423
140987044028481536	trumplover985	1724518164
983442195099037726	mvburp	1724518594
774733373209575515	hiscutelatina	1724519224
1160907025434279976	0e31	1724519432
1021219863508828202	slatthoe	1724520380
1176720386184978455	trasky21	1724520621
902263424602501141	_reflectandchange	1724522318
839536434141724723	marianmain	1724523496
1189268345862770738	11010011110110101110101	1724523678
1230723105173934130	alexithymiaa.	1724524494
1133578686424162454	uuxrz	1724526212
1238719946091925572	wetonvc	1724527588
970853217384685628	kuucide	1724528806
1228063318254555248	strawberiies.	1724529808
1094391124220727426	bdsmbunni	1724531225
1096167139557265439	tiktakboem	1724536219
1143632676822192249	guiltyplweasures.	1724536698
803002264858918942	manipulati	1724536951
740609820515893308	wriothssley	1724538205
1261515738590478461	addis0664	1724538508
1099749604381175898	mrproximaaa	1724540240
952682568304717864	penisgobbler.44	1724540506
740467525615222834	illuminationss	1724541982
921793987575156767	m4li.a	1724544238
853008245513781269	halohrt	1724545574
1231889211888631888	tookthexanss	1724546874
1083189212691562518	whytheysleeponkyra	1724563582
1139390815790174308	sansfan__20659	1724567370
963311140996280320	twinkieren	1724577684
927482228622123050	rizz.got.me.	1724584209
1234568712829407362	kiki4youuu	1724369460
1096081746937794643	.minajj	1724371800
1075278412647780462	mostconfusingperson	1724589487
1115043205805781032	cut3syvmp.	1724374847
918231212236091392	deadly_corpsee	1724376306
1010288177216487454	kayleebr00tality	1724376381
787800951406329868	farcries	1724378036
1216708609883377746	cinerup	1724378121
958614204846342194	astwpy	1724381177
1255691980323950695	103846291	1724381627
847146645170290741	ranzobr2006	1724384652
1030724923955617903	nyancatlover100	1724600104
402283148974620674	pressyoissue	1724389930
832005196095291463	yslonrai	1724601095
1116780276366983198	miiyukos	1724392213
252476495409184769	unhealedbruises	1724393891
1147899646602121216	robot_404	1724603902
1088072256862814268	_jkovrl	1724398058
1266198778822787093	egdroyalty	1724604865
972215642830807040	cwuremysrrows	1724402257
832670297421119538	carvedtorso	1724406567
1183542811379912828	_.dollieswrldz	1724409825
947590442910879774	b0ht	1724605136
1273502525219147893	hanilafvx	1724415241
913035863460577300	its_me_.jesse	1724606591
944551276597874708	cobra_neagra1973	1724419086
811738111737724948	nyasreveng	1724420977
1236143144740061216	vexblader	1724421982
859897950943051815	ivorysillegaldontyouremember	1724608249
996068864733487134	wooqs2turnt	1724427188
1148177128744042548	stuffyies	1724428155
1276568092574617746	tenacious_hamster_53586	1724431057
1185439181909020813	shotxzera_31133	1724432992
1255646102842114100	wasdsafws	1724433334
1177714539249279146	cutesubmissivegirl234	1724435973
1274540031578603550	fadedasl	1724438983
1226984021268107332	heckermom10000.1	1724439616
504802190301462528	elpepeneitordestructor3000	1724440278
1268601359314321564	_6969696969	1724442406
1274441389391745078	mlsdolls	1724443744
992311232889638923	twirlin	1724445530
857306852529274881	rootlessness	1724449821
1182647110676525107	rapperslifes	1724451369
1210208412126941206	frankoceanenthusiastt111	1724452251
1118024600152977549	lostblasiangirl	1724453251
1275604672396132352	aydedi	1724454851
1186686236837019739	deathcuts	1724457221
771514762541924413	sorrowfultears	1724459176
917450821334097970	wayvni	1724461949
1252694355429294210	jeajea.x2	1724462487
1179605209090117758	itsygf	1724463332
949666391903068212	jheneaikofan1280	1724463486
1180124906667642954	royalswerv	1724465011
1229964065749860382	traffickedkids	1724465987
1267842805720547372	frostyandfrosty	1724468624
951247806943854603	mathgamer927	1724469385
1189998280529154212	inactive020824	1724470851
719360543709986816	pexx305	1724473778
1231004827337621515	jvnyvl	1724476392
781532207901835274	hallowdeaths	1724480849
476959576428773386	biggeststarbucksfaneveriloveitsm	1724481062
1258956442472288370	costbenefits	1724484523
1276790716529381430	withyourmans	1724485473
1247731786675519488	kill198	1724486437
1107914892566077490	pwawzz	1724489574
947241287013261372	yugi.maa	1724492120
1221827796255641731	ConversAItional	1724492955
1118202419113889842	_leaaahh	1724493330
938047682298122241	mefstotel	1724495900
1086693357675364392	theblack_swan	1724497828
1274805778665967636	kemarris_ocastionnn.	1724499696
953862363877105684	dr6ad	1724501414
1168783166480334849	qxthwicpp	1724501641
1159617846691766292	i.love.dom	1724502346
1224098826764161049	.doggylover.	1724506560
1191875299089072301	lianxtdoor.	1724507767
967304296855126026	nobansoloquieropapulinsas1092	1724509225
1103387005309689946	kits_i3	1724510607
941073160390975510	dossie._.sun	1724511557
1233744707079634995	katenaticss	1724516002
1272978698252845066	gent.violeison	1724516061
1158048922044993546	.hoodplays	1724516957
1163820619251585024	typeshite	1724519269
1178327327080460309	catthatsinaschmitt	1724520440
998033331570610270	wwhs.alix	1724521070
1276807868955496519	hateskid	1724522730
852588363588567111	saulgoodmanreis	1724523723
1150240783492972706	filmnem	1724525274
1204434249256800306	abby.dies.here	1724526915
1112684704366329957	r4koo.	1724527984
1016532266358427679	.diegitomaradona	1724529286
1204927065820889178	daniel.v3	1724532941
1267274299245596805	getactive.81	1724533867
1260991703297298575	littltoddler	1724534065
871585003119738952	forgetting.u	1724536305
1111495293079408671	chuckyywackem.	1724536480
1244255276878528562	.ilovemywomen	1724536737
1191765313738522674	evvlla	1724537032
998863001987850361	mitsuki._.miyawaki	1724538160
1057407267416318062	siredtochloe	1724538995
779399062369206273	lwustic	1724539652
958036562241785897	pwincesskeira	1724541295
1239342888358252585	hislitlkiddie	1724542475
1136445614549385267	_alr3	1724547289
1173653613348933793	koalaakoa	1724548040
904036859020193912	staywithme027487	1724364466
772662956004868126	izuraeru	1724559130
817150149737971773	ajnaevis	1724564446
1217254055575814174	zyzysnatched	1724564460
1273044101599723542	ischkyros	1724366336
1220202419275694101	001101010101	1724573076
1117512536108048555	souljiawitches	1724369524
1237057908286685245	jdvibesz99x_86817	1724370383
944613184231317504	sdklgfsdlkfnsdjklf	1724371817
1209368901348229220	trustsaks	1724371946
657454985302245395	gonenforgotten	1724373520
1143481290780315659	aaaaaaoooo09	1724375008
904468186446045205	drakesplits	1724376527
760938075517091853	berlinterlude	1724379178
792069987233693716	lexreii.	1724381330
1189759407748305004	doooovveee	1724381795
1087795174744264858	basedgodpakku	1724382409
1062466815244116150	richplugss	1724382423
1098819778602344498	.dumpofky	1724578363
379310858356129794	.rin666.	1724584837
871232195711344683	matchalover17	1724388093
1082091243087073280	sugarjuko	1724390073
1272840514978451511	02923891	1724392843
1059461424893669376	regog4122	1724589541
1078293779410329610	thebabayagakiller	1724395067
1183751400216346715	cutesleepyawn.	1724396339
327557497999196162	d1u5	1724398445
1052369592007262290	alphaplayer008	1724398565
983131711753842728	69land	1724399716
1138465958210576434	wydsorrow	1724403093
1188040392684351529	worship64	1724407050
1272481922635010145	.mwenace	1724409902
1222034509625557033	bumholes.	1724412922
1037385203427065929	ilyakula	1724415573
1148274046518165625	noofent	1724416019
1168904480327225398	merasunicorn	1724417638
1190495180458049607	pocket_yay	1724418020
1262420517781114891	.slitmythighs	1724419263
1142760372655374437	567aki	1724421260
1027234056578027642	beforeitended701	1724421345
1246140456941654124	natashkii	1724422196
1163952985894817882	gunslingerdtwk	1724422305
1021362906484461598	fentattack	1724424429
1102481659154137169	staarhouse	1724424773
965569834408611870	autisticgirlsoph	1724425356
800154137912279091	lif3_is_r0blax	1724428475
736552616405893185	twothousandfifthteenvocaloidfan	1724428624
908583762084913184	.3timesskiore	1724430010
1134959879451324446	6regrets	1724430270
1221010139461586997	phyli4	1724431212
903978072171225138	34bkf13t	1724601359
1223327579612774475	ipostbaddies	1724601546
1134626785372426315	hxlaena_	1724438831
1197431388396331028	Tim's Fun Bot ^-^	1724439714
563462182285737999	complesstimes	1724440250
232623217502584852	ssaimere	1724440530
1142936420030361620	liveinsidemyheart	1724440608
1096102396419113000	rio_wq	1724440679
1276610750303047713	juanjuan0671	1724440854
1249358474710880388	onifuu	1724440990
1145824485711298590	crypto_yolo1	1724442437
1217685500207435868	cs.juniper	1724443797
788579499457511486	withlovu	1724446320
1252669866004054057	vsp.cooked	1724448420
1243308218835533824	.retreats	1724449915
1265693792325865653	inhisrestlessdreams	1724451467
934432215692087296	.ggmop	1724452324
1026189619848544277	.dearhaerin	1724453545
1134232033015644201	paidlolll	1724454903
643535707293351977	deepintomythoughts	1724605078
1152308164696490116	lacedpearl	1724456470
821051931232305194	wonyifies	1724457528
1242220835914256426	cantnm	1724459751
1211167047963385891	fuckabitchh	1724461026
1217657327109537923	cwtekittyy	1724462134
935672228614393926	desvrse	1724462541
785651608989073409	ilovemillfs	1724466004
1171217886430376007	sonbeater	1724469836
1121571529650606110	ft.vunify.	1724470971
991498608551673877	theekalypso	1724471755
1164724143992868895	xw6v	1724473843
1079189813661548636	yeonjzn	1724476629
1017520316446154853	iloveoliversm	1724478662
773000393286352978	.rikuzx	1724484716
1125377087822368788	led2me	1724485563
1148223793123295262	angelbreaking777	1724490925
1263577034639151124	bigb1ngb0ng	1724492757
1203317846650912829	soul.lua	1724499335
1223612581571199160	ffddsd.	1724500170
1254993660576137298	hwaunts	1724501544
1220429442678259722	corpzzz000	1724502379
806998841978650694	.leasznnn.	1724503062
900771749375930469	.ialoneamthehonoredone.	1724505159
780668112592568410	filthygraves	1724505192
1227056133714219018	SIMP	1724506451
867938732479762452	mcw_nae	1724507147
1057092245133729792	.clitsuckaa	1724508710
1116829805028069446	do8mware	1724509535
893327183844638781	vampireh3art.	1724510791
1189245463690489860	user037371940	1724512937
1155937774776623154	cesartard	1724514544
1258721384180224114	7burn_ped	1724517131
810659883287576616	yyseiunn	1724517963
1135497262890496010	dwollasign	1724518907
1141883135060090941	mira.cornbread	1724520676
1040984685402148864	wastelanddd	1724520753
1155956200328921088	maznyc	1724521658
1124023821553377370	p0rcela1n.d0llie	1724529718
1008065667683065896	bangtans	1724530854
1231281553703698432	adianababy	1724534707
1000447335270195220	gloxsy	1724536334
1085077970546339930	wreilltouchyou	1724536776
901531691468849152	vwvwvvwvwvw	1724538231
1262185939971870724	derangedbullets	1724538410
1196896025739280404	kamarisdiary	1724539030
1163190890907566180	6663197845504_72838	1724539655
1014581688577306644	_divergent_general_mahoraga	1724541125
990408095861723166	glockiescooked.	1724543307
1246402444309565493	heknowsyourpain	1724544769
1223320762090262631	hellcwrime	1724546568
1206020196616249424	eeheeueuehe	1724364741
798432917792882689	uree0000	1724364247
1131427367978553406	geb66.	1724564298
1133947289388449792	.giselamere	1724367290
838769590943219812	samayster_	1724568516
1112881635151585362	fakekoba	1724573168
915982084890320926	curebrokenhearts	1724370301
1232375282946801826	inshallahimaan	1724370687
1259568918142390292	dopesluts	1724372006
1187225699556266004	forspokenkos	1724578591
1055316132929740860	replaythememories	1724375211
1268289248851918909	48ms	1724376805
1100029303875444766	lushogoat	1724379614
1260482491282620479	topdawggerton	1724381362
1083473685995847740	ziionnat	1724383141
1195903305541492776	v1soflair	1724385128
972596404948205568	rapelisted	1724578820
1123430967072276520	_lv1qa	1724390410
1254967647351607416	hisfn	1724392853
1222838517567197194	yang.ent	1724395953
1259925408439341171	waikthemtotheirgrave	1724400488
1191791482416402494	fweargf	1724403274
1100511574248149072	red6x696969	1724407408
1120639236157231156	22aubrey	1724589659
937035440714838076	neshastoleyoursoul	1724413461
1233095461594992783	.3uphoriaxz	1724415657
1233938250629120077	luisunicornfan102	1724417913
1104158860245213314	almostcutmywristsforyou	1724421462
1197635042478932098	balkanperverzija	1724422410
1224455837100019839	kiyokohina	1724424551
916337117418881065	__kriki__	1724425844
1190377094111297566	zfmc	1724427840
1222913823845908630	s1lentforchris	1724428935
634213752333402113	killinglarps	1724430088
927576826128265317	.instantly	1724430260
1085399939540078673	illbwy	1724590217
1151838664079458336	jakiccc	1724433251
1173899303773806621	i4pk	1724434218
1174158595902935162	x2.kri	1724593583
898334448536404038	cursedl0ve	1724439969
896722889980670002	holdurarm	1724440815
1106605626131484773	lockzi.	1724443266
1146503574180868327	.nightwingsnum1stannerrr.	1724443990
755900536708137001	lexitheslutt	1724446718
1012122479772323881	thebopiest	1724448535
1165355330880933972	2kkyanni	1724451534
1020724911590871181	allabouteliel	1724451807
1206090426021584897	juniorhfanboy	1724452636
1164870549328109642	yukayuki0	1724454151
1123311701207548004	number2tittyfondler	1724454950
1110250557874110686	ilovemybrunetteboy	1724456709
849089317644271677	purezoro	1724599605
1139631890538696787	prince0579_43039	1724460004
1144216251737055253	bloodonmynose	1724461043
828139656473608202	feetplay	1724601462
1203860297912287304	mikans_biggestfan	1724462768
734643241520988230	capturescene	1724604044
811047675541585930	hollowww	1724465236
1126674539837927424	arithecoolest_	1724466146
1183493345910206537	zayaafr2	1724468898
1090326854340190279	g.99999	1724469845
1187313764165500939	prc12.	1724471383
884151151824633926	marmarchomes	1724472354
673618216286945300	spencer.reids.glasses	1724472392
745858717786046546	luvforcharity	1724473056
1212817473875746958	easiestpersonalive	1724605106
1254966516114522133	__.fein	1724606815
1199178701271732255	underways	1724607496
1267947352858296381	molly	1724482205
710436339555762237	kkarmaa	1724484856
1195256153651806209	hoodfeens	1724608256
1250959809516404741	5starcashy	1724489034
903521251824381962	rutayan	1724491042
1061019482082001006	rringwrorrm	1724493193
1225388482021560403	stuckinhisvoid	1724495529
1019137344927957012	lovemepopboss	1724497364
1234032758578483281	oops.sorrychanel	1724499360
1120751894852276314	myacute	1724500505
925342313927016529	sick111111111	1724501958
803416142924087296	esmesfangirl	1724501971
1157839602674057317	cvpx	1724502461
1224861162005467279	slattwontsel	1724502935
1238607185655758989	PixelPulse	1724503095
918351065051709461	deptmaster	1724503444
1259662306380484798	harrassingpedos	1724509683
1269025690175406252	stalkingyolifesocool	1724510935
1107340740721385603	tyzz5951	1724513165
839502492513206302	keepmygen5	1724514634
1245922306346320003	sealslut	1724517359
1152621529906036748	jahmarii2jiggy._	1724519100
899659030413324318	zaadpiraatt	1724519940
1202131352745693256	vverrsatile	1724520807
1133652640274858125	twistedbodies.	1724520925
1264588466197495859	justsomefemboyslut.	1724521942
1263858485339230208	ylnyo	1724525924
1044499905978314813	hollowpoint09	1724527560
732730543019655289	4evalayy	1724529755
1034982666224812043	irlyeojin	1724531009
1234862531303047208	soulhours.	1724533594
487026109083418642	wormylover22838384627	1724534774
1001270543040917537	ycbwq	1724535971
932683928710578208	artsoulja	1724537455
1122568247712161973	cutmyself.com	1724538330
1240358375573815448	hauntingyouxd	1724539958
1184267146486882449	687k	1724541793
1137353231748583516	elsokibai	1724543698
1102769389780078692	dadaslittlelatina	1724546640
1089772886098706494	fucccraw	1724547928
1134675027774689401	uxwi	1724548501
1161772932335403119	ruinlaw	1724548761
924736509226123304	wu.h	1724548985
1170854488869965856	FS Embed	1724549005
1165849763745386587	6xka	1724549299
1203695834231869564	pradaxox	1724550445
1025537449696444457	10mmss	1724550612
1255909954444070965	batgawa	1724550689
414903775719981076	cl4ssist	1724550899
1244314385577676927	chasehatesyou.	1724551385
1126692607368638508	vinsmoke.112338	1724551455
961458226434560010	pftr3xse	1724551824
1028350218946744492	lvckviv	1724552382
910379516826886154	bloodylmao	1724553029
1017486033107046493	sqtxz	1724553348
996471504332144753	hailrin	1724553479
1246380245272231987	comptoncord	1724553988
753761271328931871	steven0rwtv	1724559740
929914955854147674	morenotrapper	1724554641
954820826308427846	i389	1724569561
1216305893612847184	mwnyunbae	1724554727
1116553278122102894	they_fw_yuji	1724554887
1118983484615184557	thisisntreal	1724554914
1011718826926297119	starz_goatfr	1724555093
1149092344549875834	ionbeef.	1724555432
866005702458736651	tiedtoyou	1724573255
1005575768081965157	dvllface	1724556242
1226646495416156292	pynklxv	1724556316
1049889727865700432	buriedinhongkong	1724556632
1238915791362064394	thefxxx	1724556683
862758996950908948	.3omi	1724556840
871178864720740375	luvy.amani	1724556959
769976371161071656	feenin4wock	1724557219
811806941226598450	best018052	1724557373
1057051641607630888	3kbd	1724579198
813627889199087616	t4ken5	1724557412
958006336363331625	mwyst.	1724586218
1056267249092145203	user171736389176413	1724589977
997228341352480791	kyarax69	1724593731
849258304911573052	kr1pticz	1724595014
1151319279946448916	johnsi09	1724599645
923303155960270869	wfluvx	1724604120
784577646259994654	pinkmodelsex.	1724606826
880990684952281158	elgabe.19	1724607138
1070871274043211776	5tackaaz	1724608390
1251006603558125605	relived01247	1724609736
\.


--
-- Data for Name: premium; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.premium (user_id) FROM stdin;
1074668481867419758
1272545050102071460
1272516805478318082
1272521861997133915
809975522867412994
461914901624127489
1082206057213988864
1278351922826448906
1278350907599491226
1278350626052374599
1278351365407641761
1255612726718500864
1140301345711206510
1083131355984044082
1258409203748442206
1171311287825879107
1291994246051663913
1292007787039166484
1291930859657760973
1292271528599359538
1291751342045397053
1291965890400747524
1291161973148483644
1291772893239185452
187747524646404105
\.


--
-- Data for Name: restore; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.restore (guild_id, user_id, role) FROM stdin;
1256851790540832831	187747524646404105	1256851790540832832
1245364433065218098	1251522055233339412	1246087771572011039
1217257999056371812	969988151730896977	1217373538835501080
1217257999056371812	1019382652203188265	1217373538835501080
1021118760846897312	535590447423422466	1224746674061053953
1217257999056371812	1272210596804165673	1217373538835501080
1217257999056371812	1263136190656282849	1217373538835501080
1252079052823593050	1165355330880933972	1252768436929429606
1272020420760965140	624030964263288833	1272036621344047184
1217257999056371812	1104652949029928980	1217373538835501080
1217257999056371812	861327881955049479	1217373538835501080
1217257999056371812	661653221646794782	1217373538835501080
1194496130134851664	1238315184020525141	1248676977293000774
1268850200370217043	846798070180347965	1268859402669002753
1153678095564410891	701498672642392236	1208980183512522794
1217257999056371812	1008159836967555073	1217373538835501080
1021118760846897312	1003433295222145054	1264057888607965218
1226492622617444423	637492885289304085	1227139363360477204
1217257999056371812	837668330894131220	1217373538835501080
1217257999056371812	1222656838504419479	1217373538835501080
1152334664153960509	1208825174288236554	1221809460452790292
1217257999056371812	1081580678472286338	1217373538835501080
1244403114447212564	407679133603069954	1254787640922996878
1251212297108586608	1220759514769260625	1251332804244013097
1217257999056371812	1220912743633391646	1217373538835501080
1254645708611518495	1236069662194929725	1264406832739516447
1121701387303137370	1236069662194929725	1247395598471135354
1217257999056371812	991756642385412166	1217373538835501080
1243841990525849631	1206712796960657538	1265433197219418152
1243841990525849631	879898345605304351	1265433195009151058
1256881462456877076	1084937449379209307	1270516533273165904
\.


--
-- Data for Name: restricted_words; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.restricted_words (guild_id, word) FROM stdin;
1183029663149334579	faggot
1183029663149334579	bum
\.


--
-- Data for Name: selfprefix; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.selfprefix (user_id, prefix) FROM stdin;
1035497951591673917	.
1269597022634119261	;
1250382435632418816	;
1169601140804042842	;
878363386918862888	,
1010919763230339102	|
1175195486605561887	,
957771692300709918	"gay "
750379503179661444	
1074668481867419758	
1251138585789337600	¥
605995776711327769	?
269910607174696970	!
971464344749629512	;
1082206057213988864	meow
1198625732327374909	☆
807387522543124520	|
1267726635126358048	.
1267440086673522691	;
1140301345711206510	sex 
713128996287807600	dildo
1208472692337020999	sex 
1273201960685928468	neca 
1262799073077891155	,
549804055275372544	,
819337895877279757	mont
988301749041397760	,
1134945178407424000	,
1243912472956637246	,
1280162916158410875	^
1099719762487025774	.
1052362761335738398	-
\.


--
-- Data for Name: starboard; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.starboard (guild_id, channel_id, emoji, threshold) FROM stdin;
1183029663149334579	1274088996519022714	💀	1
1247448738067386379	1278477434651414590	💀	\N
1268584157639082086	1279158395164692664	💀	2
1244403114447212564	1279165138238439477	💀	2
1173253101906563102	1279577954397192263	\N	\N
1212420500366557264	1280985803664916564	💀	\N
1279436042583408671	1281648966601019444	☠️	\N
1282393410204078141	1284176546718023823	💀	2
1284475167703171114	1284483583691718729	💀	1
1284532619383672853	1284534350603489485	☠️	3
1282926708650938410	1284537927036309534	💀	2
1241058950145769482	1284896912989749340	💀	2
1121315810892316754	1121315811961880732	💀	3
1287161213502881874	1287166035602182225	💀	2
949837695050469456	1287450167229812787	💀	2
1206215747869614122	1206215748360343586	💀	1
1290472403763335220	1290818739381600316	<:6696pinkribbon:1290473919148462161>	\N
1260459692426006550	1280237253150638111	💀	100
1283713863589564457	1290263218266046514	💀	\N
1293699972172091523	1293709240095084616	💀	3
1232760919113863279	1294139746628407377	💀	2
1266853535887392841	1288933946406469736	<:coldShock:1285866323057971221>	1
1292282920156794932	1292520527717466152	\N	\N
1296538895030161448	1298203780155834389	☠️	3
1298459389220622368	1298479014717030410	☠️	3
1280214704626728990	1299002472374997093	💀	2
1291961786852970558	1300638877106700389	☠️	5
1119311424473276416	1302001290376646848	☠️	4
1292861168054046831	1302115796566409258	💀	3
\.


--
-- Data for Name: timezones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.timezones (user_id, timezone) FROM stdin;
111646804658921472	Asia/Singapore
355863745341423616	GMT
1278250011431534593	Asia/Manila
809975522867412994	Meow
1243274323402293259	Europe/Dublin
1247387601858723920	Asia/Riyadh
1273201960685928468	America/Los_Angeles
1262799073077891155	Europe/Amsterdam
1083131355984044082	America/New_York
1185934752478396528	Europe/London
255841984470712330	Singapore
1257668104016760902	Asia/Tbilisi
710993692764274728	Europe/London
1284922928298852373	GMT
394152799799345152	Europe/Bratislava
330506093652344833	Asia/Jakarta
1222251039726501980	America/Los_Angeles
1142780447697403937	EST
877908381900345344	Turkey
1135640220944056360	Turkey
221025167684403202	GMT
187747524646404105	Europe/London
605995776711327769	America/Los_Angeles
153643814605553665	America/New_York
783781258827268126	Europe/London
1287527095366451262	Asia/Manila
1252343511571759149	Asia/Manila
878363386918862888	Europe/Brussels
1232638538697146461	Europe/Bucharest
1256161082188234804	Europe/Budapest
1255491580815605790	Asia/Tbilisi
401770464017514498	Asia/Baku
814657545305194557	Europe/London
606925094899417099	America/New_York
1147238281625477202	Europe/London
1049824125536960523	America/Toronto
1139841273281392640	Europe/Madrid
856298738044895312	America/New_York
1281466042354499584	America/Denver
1298228908529029122	America/New_York
643054595983015977	Asia/Tokyo
1039235889785733130	America/Toronto
1104828832919330816	America/Detroit
1226672702761472020	America/Chicago
1196836362880548866	America/Los_Angeles
\.


--
-- Data for Name: topcmds; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.topcmds (command_name, usage_count) FROM stdin;
vape	78
bible	11
enablecommand	1
links	1
joindm	13
modlogs	5
invoke	6
stop	514
flavor	211
softban	7
enable	60
resume	14
bots	12
blacktea	34
shards	71
pin	5
joinposition	2
starboard	17
boosters	9
skip	871
attachments	1
dominant	27
login	40
thread	2
vanity	21
voicemaster	48
wave	4
icon	2
lastfm	64
logout	3
disable	20
stare	2
pfp	5
hit	1880
activity	2
firstmsg	3
view	135
server	1
customcommand	3
stickers	1
shell	53
addemoji	194
api	11
levelling	47
urban	58
override	1
invites	23
weather	59
test	92
loop	25
autorole	32
text	53
pip	13
remove	116
userinfo	145
levels	18
filter	22
set	367
name	1
base	3
restart	23
create	41
clearsnipe	191
banner	187
threshold	11
roblox	178
git	12
nowplaying	59
message	93
voice	112
unload	3
tag	2
jishaku	35
google	75
howlesbian	230
list	24
inviteinfo	30
rtt	2
selfpurge	20
flavors	98
unmute	42
dm	9
embed	70
mute	110
commandcount	3
removebg	30
lock	423
tracker	16
instagram	83
blacklistguild	1
twitter	9
membercount	157
cashapp	58
invite	42
volume	177
push	22
prefix	50
unlock	189
boosterrole	18
say	3
poll	7
joins	20
selfprefix	19
shuffle	7
py	76
slap	10
roleall	18
enlarge	5
serverinfo	110
botclear	61
howgay	701
vanityroles	35
setup	99
unban	60
gif	32
source	19
image	148
ban	252
welcome	64
uwuify	58
hug	8
shazam	77
bird	7
debug	14
logs	60
unblacklist	4
leave	16
usernames	31
uwulock	63
snipe	402
rename	1
imute	2
iunmute	1
kiss	15
inrole	28
user	50
cat	4
tiktok	37
ocr	29
boostmessage	11
kick	33
gi	5
leaveguild	2
blacklist	6
pause	36
joinping	32
oldnames	8
bans	6
editsnipe	22
variables	6
poke	2
feed	3
shoot	4
tickle	10
disablecommand	15
nuke	95
colour	1
delete	3
autoresponder	49
chatbot	15
sync	24
system	2
load	138
8ball	322
add	104
botinfo	439
purge	580
sticker	2
reposter	259
globalban	5
channel	116
uptime	14
role	648
avatar	714
screenshot	54
pack	47
ping	296
dog	9
emoji	13
help	737
afk	704
forcenickname	61
play	3856
randomfact	8
timezone	83
chatgpt	304
ship	32
\.


--
-- Data for Name: usage; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usage (amount) FROM stdin;
\.


--
-- Data for Name: usertracker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usertracker (guild_id, channel_id) FROM stdin;
1257987786888318987	1281151331561639956
1120434472114999307	1282018133736947815
1278420379211399249	1283086527378886677
1282811507373113354	1285654785781010462
1244403114447212564	1280261488841592874
1278315918501351486	1279627564004147301
1285256239520940107	1285299763859685447
1212059022254145656	1286350457752522895
1078139875573899387	1286015858287579208
1283124591048527892	1287471776393203844
1283900068876779583	1289064673957777459
1260459692426006550	1260473181412786186
1289603576561401958	1289637760109379665
1260827368625279159	1289764334439764054
1287252826556469371	1290019708803874866
1281274638567080018	1281275585338937528
1143814427813085184	1292166510655045772
1175584188758507641	1291916340025753671
1281634482918789212	1282171875132313682
1295757329350004747	1295757531288965153
1284903610894778529	1295760757220315220
1253839169965527190	1295873593665650780
1296041301858320478	1296042334445764620
1294572524171952168	1296214090879991940
1250626268907573309	1296226285231542354
1270162679771824231	1296622125573996594
1297293375204229120	1297399930473676843
1194362193991446603	1254164614267273398
1281400518073389068	1297583179443732540
1121045839012438027	1297670454621896754
1299033953499353158	1299033953499353161
1295533858615328811	1300628754397270037
1233168080339865723	1296771103309565952
1301701045482950766	1301701046069891124
1267619083013328958	1302316637000564797
1302632048145600602	1302632048934125586
\.


--
-- Data for Name: uwulock; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.uwulock (guild_id, user_id) FROM stdin;
1263195476245610536	1272545050102071460
1281680936316178482	1269229334175158293
1153061964633882685	1053168651198537818
1153061964633882685	1193707690157944903
1262477534482665492	1208774810805739570
\.


--
-- Data for Name: vanityroles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vanityroles (guild_id, channel_id, text, role_id) FROM stdin;
1152334664153960509	1261384962637299884	/rixx	1258850718622945291
1224825543661453483	1275818724212871209	\N	\N
1255241667997601962	\N	/copy	1256008227255091230
1263146753109266534	1271438576701145181	/called	1265364918375420058
1276605260110237758	1279961677441532017	/yuko	1276605260110237760
1279999537691496448	1279999991196422175	/healed	1279999706835058748
1267378542874853549	1280358979343487006	\N	\N
1183029663149334579	1274075071945900082	/testing	1190703635638784172
1244693649753641013	1244693650567463015	/sweetheartt	1262553844945129553
1270486377460404356	1280110981124587633	/avoid	1277098075172900924
1244825571716759562	\N	\N	1244844127112138812
1267836668388315168	1281089061364301928	cute	\N
1240333469758914590	1240333470191063143	\N	\N
1255969204205523004	1256991787612901487	\N	\N
1276302538152611972	1278268966653132835	/flirt	1278269327488843816
949544575620509706	1240220542368481300	/trapstars	1278815898131497033
1268584157639082086	1275891304588509296	/past	1276818378299801631
1274454080286232617	1282070114245541919	/stabbed	1279503469631373314
1275204588894683247	1280291574131064844	/pilot	1275244574989877324
1251594471531876463	1282526239114006558	/ayaa	1282526160873590795
1282563196120727663	1283112943181107200	/strict	1283113064006160405
1281680936316178482	1281680936337018940	thanks for repping /swore	1281680936316178490
1274781210475892756	1277708489728196770	\N	\N
1274220522426732554	1274220522426732557	vanity	1274221922007253078
1121315810892316754	1284650357686927463	/gakko	1121315810892316759
1294238490510233664	1294287713851277355	.gg/forbidden	1294285267087396905
1267992274130702417	1285000028523462738	.gg/legendcityrp	1284976313265819700
1285074920627507210	1285074923458527325	/all	1285074920690155588
1281413288449540181	1281414396844970004	/cutter	1281426813607739392
1271624140905779241	1271627219051216959	welp	1296257495748050985
1286694780121911347	1289956843682005012	thank you {user.mention} for repping /offroxys u now have pic perms	1289956529537290303
1292985929954365472	\N	rep for pic perms	1292999465761902636
1285599550991630406	\N	\N	1285605877381861427
1279991388808806461	1289684311984832562	/sixeyes	1289771562702082189
1266853535887392841	1279740780705222720	/223vz	1267203048254603465
1295814990590382170	1296596109191544953	Profiles	\N
1287252826556469371	1290028172796231792	car	\N
1295818113056510052	1296210022740656230	.gg/enlighted	1296640842177712188
1132513607305920522	1286710786626162798	/barcode	1212250121333645322
1283618825517928488	1284917943091597362	/nurse	1285422593595281418
1273415265433948250	1290042392174657577	/sws	1273690608241741965
949837695050469456	1287459838653370470	/shots	1287459704817319947
1290516120050335785	1290517026690830406	\N	1290516120050335785
1283124591048527892	1284671846347706373	ty for supporting <a:1146_dance:1286562751866736701>	1287731618563231754
1118862694980788276	1154757916717498398	/6ure	1283627752229961800
1255886807032135721	1279888173870088296	\N	\N
1289659056159719577	1290645631089512550	test	1290626933041791001
1290472403763335220	1290818668183425115	**thx for repping /rafts cutie patootie {user.mention}**	1290818494442508443
1221529993318891520	1279868483789918341	.gg/bigwheel	1249378918528581795
1293699972172091523	1296943507998769162	/remains	1296897652327186442
1285832779216719967	1285862042825265202	/arent	1286139358130212954
1281400518073389068	1297417042261180488	\N	1297413122931294309
1245033545932476416	1249320231021580298	/husts	1245108786646089829
1260827368625279159	1289295542836527144	thx for reppin loser	1289295397067685898
1279472645661917347	1289988155327512587	/chihiro	1289987357243605034
1289647774685466654	1297587818394288189	.gg/voidevil	1292399602397614152
1289603576561401958	1289628828876144660	asd	1289632935930105971
1282828551418019872	1293562924572610641	/are	1293563109432365056
1297280005562175488	1297640312730292315	Thanks for reping /night <a:cig:1297632027285258355>	1297639777369329705
1291045381739905105	1297905805647024158	/coma	1291053236891160647
1296538895030161448	1298198070701592586	\N	\N
1245364433065218098	1294664095446077522	/4kuma	1265265375575277599
1296646561237045268	1296648366624608337	\N	\N
1262461978031423498	\N	h	1299014111039983656
1291285872666345503	1295389307338752051	.gg/naxro	1295390985844559955
1070762079985877102	1293873553740927016	.gg/hustled	1293725760057774090
1287508279064399953	1295164215429959761	/band	1288834387693273181
1214726898563813406	1295990442294513674	\N	\N
1281381630014918736	1281410720671731733	/worry	1298143760433156147
1291961786852970558	1301814959008645141	/bounty	1294110286269120542
1177416209990418443	\N	\N	1292956040639549470
\.


--
-- Data for Name: vanitytracker; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vanitytracker (guild_id, channel_id) FROM stdin;
1224468938260484156	1275663475330388050
1257987786888318987	1281151551880171540
1120434472114999307	1282018514517098597
1278420379211399249	1281043041041387552
1272301892776755210	1283414063904198746
1244403114447212564	1280265695892082829
1212059022254145656	1286352366970343428
1280513047458484416	1281019874189246518
1194362193991446603	1194362194457018471
1283124591048527892	1287788044824477801
1283900068876779583	1289064256532123688
1260459692426006550	1260473098453651568
1289603576561401958	1289638460164149298
1260827368625279159	1289650288164208741
1287252826556469371	1290028172796231792
1281274638567080018	1281275585338937528
1143814427813085184	1292166510655045772
1056658126180462683	1057789043888377927
1293558005962510406	1293586928532324459
1278068842119172148	1278068893486813267
1143665213170782228	1294844581069983818
1294870137903517737	1294888046952579162
1281634482918789212	1281849225084403775
1293699972172091523	1293706802206085193
1297293375204229120	1297399959230091284
1281400518073389068	1297583175895351326
1121045839012438027	1297670374359568426
1298459389220622368	1298489664239571037
1274781210475892756	1299351613978443868
1295533858615328811	1300627894132932618
1267619083013328958	1302318993138520185
1302632048145600602	1302642481376137226
\.


--
-- Data for Name: vape; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vape (user_id, flavor, hits) FROM stdin;
728293412595302402	Blueberry	\N
1035497951591673917	Strawberry	7
1226608436343734272	Watermelon	1
461914901624127489	Strawberry	1
1173718661320675339	Strawberry	12
1266377266892505100	Pineapple	1
894275668110622771	Watermelon	3
1211082272393138237	Mango	21
1252236665099915411	Watermelon	2
611339099122434062	Watermelon	1
958036562241785897	Tropical	2
211069788544434178	Grape	9
1177135670586781716	Blueberry	1
1266170489546608672	Watermelon	1
1237087452385120337	Strawberry	3
1108699099705913436	Blue Raspberry	2
1111836539736035359	Strawberry	1
1173121628457156690	Strawberry	1
1137710319666470912	Tropical	1
1211110597345812501	Tropical	48
617249450867425301	Apple	1
1269255506753617963	Blue Raspberry	124
1239310028901580864	Blueberry	1
946513696920850502	Blueberry	35
1070676187942232165	Mango	1
1179756970530570300	Strawberry	10
1208328032843071581	Tropical	\N
549804055275372544	Grape	6
269910607174696970	Apple	1
665262642855673887	Watermelon	1
1176490404611379284	Blue Raspberry	3
837046085834113074	Mango	2
924660024968634428	Blue Raspberry	1
713128996287807600	Tropical	5
1183890576177909813	Pineapple	20
1171101755413626945	Pineapple	1
1260736524035817595	Apple	4
894786396659793920	Grape	12
1275754193919152129	Lime	1
993245909079052369	Apple	2
1141124521722663023	Blue Raspberry	\N
1165787541853704305	Blueberry	2
714637703282688091	Pineapple	1
883103022538956830	Lime	5
1279679218053021721	Lime	2
1163080789957812285	Mango	1
1251138585789337600	Blueberry	1
643827079150043147	Mango	\N
1231725751875801148	Grape	3
897042672349495307	Mango	208
710993692764274728	Pineapple	32
1262943338340945920	Lime	\N
1085591641529778260	Watermelon	1
249708064654098453	Blue Raspberry	\N
1266717995556798516	Blue Raspberry	1
1149271973197787236	Pineapple	3
1263737585180868711	Strawberry	41
478547060275150851	Watermelon	4
528867294038720533	Mango	1
1030588830786539531	Strawberry	2
1025779499259928577	Watermelon	\N
1203274875792392223	Watermelon	\N
1185610934912299038	Tropical	\N
1249852606524821605	Tropical	\N
835102082372599838	Strawberry	5
1200812877217546313	Grape	6
967296843417530481	Grape	1
979019915925278740	Watermelon	3
1272370013143040083	Blue Raspberry	\N
1149133042275856435	Blue Raspberry	1
1268709178072109058	Apple	1
1190607328190402574	Melon	2
1264405618366742534	Tropical	1
1180365000628510848	Mango	10
1286715329682341936	Apple	1
1093224895728595075	Watermelon	1
1275011876224237663	Apple	309
1182815168321835151	Tropical	\N
1019350568512278640	Mango	4
997012189804232734	Grape	46
1138582022361718894	Watermelon	1
875439738088210432	Blue Raspberry	95
1026345085543137320	Grape	2
1288274433747845205	Blueberry	14
974360599347753050	Lime	3
1274169607862747322	Mango	1
1106703744458039387	Watermelon	1
1163395242075115520	Strawberry	19
1184109762040836176	Grape	1
1180286708537901258	Melon	1
924339247421481011	Mango	1
948386554173329408	Strawberry	8
1168984521606185031	Watermelon	117
1184991444755288125	Blue Raspberry	12
605995776711327769	Lime	29
874069363458727997	Watermelon	4
1283050572370415702	Blueberry	\N
1071793400694706256	Tropical	2
1200284154340847667	Strawberry	75
774391636313899018	Watermelon	15
880529506224439296	Watermelon	8
1194184813117186048	Mango	76
871149817697550367	Watermelon	3
1247282517288157347	Tropical	1
1242603693434470494	Watermelon	7
1159604244006051880	Blue Raspberry	1
872101474929373206	Strawberry	1
988301749041397760	Grape	\N
1116206291392663602	Mango	1
1015908496748843058	Melon	40
1202082984409174096	Mango	2
564318170115211266	Blue Raspberry	11
701713839225569280	Lime	2
689646228098908215	Watermelon	1
1257389817113874546	Strawberry	3
1281061217384792186	Blue Raspberry	1
1186924385198673930	Blue Raspberry	353
1254355023341682739	Blueberry	\N
1284922928298852373	Strawberry	1
1175063383645618256	Strawberry	1
1264596605252796426	Blueberry	18
1141171402616094792	Blue Raspberry	1
989668169029394454	Mango	630
1232868444555317331	Apple	230
1217119921666785341	Apple	7
1077200872167178341	Lime	20
847539615589859344	Tropical	7
1234208916129452092	Grape	6
1232182630670139482	Watermelon	3
1215472620334747710	Blueberry	8
1029081775084937287	Blueberry	3
734657421590396940	Grape	2
825731526523224085	Strawberry	2
1006926194844909618	Blueberry	4
963265648354529300	Strawberry	6
1183464733563699321	Mango	76
609245913310953492	Apple	12
887497695730729001	Mango	10
1247743426699460676	Blue Raspberry	3
1123240248709754990	Lime	245
1204201147393507349	Mango	23
1111508285502267452	Watermelon	108
1199337675665190982	Blue Raspberry	8
1271360685942771713	Blue Raspberry	2
1271796878555484222	Strawberry	1
1021850107425071144	Apple	1
1043272912217571388	Watermelon	3
879921749850988574	Blue Raspberry	\N
772133911022534666	Grape	20
241568842344562689	Blue Raspberry	4
1191104689178152972	Blueberry	6
1152771520763015228	Apple	4
1171969258427793428	Lime	6
347532500970635285	Mango	1
1181129149818089487	Blue Raspberry	5
850387045398478868	Blueberry	3
1122984949541257337	Mango	1
1274881339547717663	Blue Raspberry	1
529782956168970241	Apple	3
1231279389879046224	Strawberry	4
994213907570888754	Tropical	7
1028331684770365442	Mango	\N
1246379169651228697	Blue Raspberry	2
1295578052016996494	Watermelon	2
1142780447697403937	Strawberry	15
153643814605553665	Mango	1
1031258464338579607	Strawberry	\N
1202487527659806725	Mango	1
987248021341343765	Grape	1
1064854600076763188	Strawberry	40
1039678567467978863	Tropical	21
1280692394320461918	Strawberry	20
1219547995155071050	Blueberry	52
1267843992637407355	Mango	\N
1277330614122451006	Watermelon	16
1252343511571759149	Blue Raspberry	61
1300363472772796459	Tropical	62
1120169434678566964	Lime	2
1127544949857071225	Strawberry	5
1088668944476405891	Grape	1
187747524646404105	Tropical	43
1061285129009508463	Apple	2
1300349991667236910	Mango	30
1256821173363413102	Mango	23
1064319948182261801	Watermelon	2
1287908663906009127	Strawberry	1
1185423230715056213	Grape	64
1197652148947787867	Mango	3
255841984470712330	Lime	4
524780254347132928	Blue Raspberry	1
192080653079150593	Mango	1
1257414583711170693	Tropical	16
969967072358592554	Tropical	3
1076579307910082701	Lime	1
941168660981116991	Strawberry	2
1301297353226977334	Watermelon	2
1277583622026825740	Tropical	112
1273847506211700746	Watermelon	23
759578139772583957	Tropical	20
1201666560507248681	Apple	7
1177858886116573210	Blue Raspberry	16
828713485012959283	Lime	99
1283648607341514828	Blueberry	2
856298738044895312	Mango	1
1126405340007772240	Blueberry	26
1298228908529029122	Blue Raspberry	2
1280557262510751849	Strawberry	\N
1287527095366451262	Mango	26
1239331582465146951	Watermelon	3
390531922247286804	Grape	5
1279960052647596082	Watermelon	1
1206454754750890046	Strawberry	2
1264692621654233160	Grape	3
\.


--
-- Data for Name: vc_stats; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vc_stats (user_id, total_time) FROM stdin;
\.


--
-- Data for Name: welcome; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.welcome (guild_id, channel_id, message) FROM stdin;
1279205866993877085	1280576488135200910	{embed}$v{content: {user.mention}}$v{description: <:white_rules:1280574356891897856> ・[tos](https://discord.com/terms)\n\n<:wine:1280569559539253259> ・[pfps](https://discord.com/channels/1279205866993877085/1280575052395581450)\n\n<:loudlist4:1280574405172400200> ・[polls](https://discord.com/channels/1279205866993877085/1280563043335536722)}$v{color: #000000}$v{thumbnail: {user.avatar} }
1278420379211399249	1279567209823342614	embed{content: {user.mention}}$v{author: {user.name} && {user.avatar}}$v{description: \n **wlc to @appear <:3333:1278837517512212613>**<:6_:1278834467221278722><:6_:1278834467221278722>\n **rep or boost for pic**<:6_:1278834467221278722> }$v{thumbnail: {user.avatar}}$v{color: #CDC0C1}{footer: {server.member_count}                             \n{server.member_count.formatted} member}
1262372126325997609	1271113853803036827	Hey {user.mention}, welcome to the official support for Lost bot.
1152334664153960509	1256764041607778425	ㅤ ㅤ welcome to Rix Lineage <a:1a5_whitebutterfly:1255176130105835700> \n              {user.mention}\nㅤ
1268584157639082086	1274043867586498634	{embed}$v{content: || {user.mention} ||}$v{description: <:blank:1278751077302407178>\n<:blank:1278751077302407178>\n<a:0000000_sprkl:1274023855236579339>  ﹒[past](https://discord.gg/past )﹒[wall](https://discord.com/channels/1268584157639082086/1270696859865972738 ) ﹒[chat](https://discord.com/channels/1268584157639082086/1274043867586498634 )\n<:blank:1278751077302407178>}$v{footer: /past in status}$v{thumbnail: {user.avatar}}
1279837686542368880	1279837686542368883	fuck u want {user.mention}
1268305462890205269	1270872046196490350	{embed}{description:diahreah!}
1272292232250265731	1272892233342910545	welc {user.mention} <:0105:1270720317966389391>
1276605260110237758	1276605260353245310	wlc to /yuko {user.mention} ,  stay active
1276302538152611972	1282108232071905280	hi {user.mention} inv+boost and be active in vc's https://discord.com/channels/1276302538152611972/1282108406412476468
1274467574842658928	1274475173654827039	{embed}$v{description: Welcome to **{guild.name}**!\nCheck out <#1274476317961883658> + <#1274475191405383812> to get started.\nOnce verified you can check out <#1274475316819136593> to meet new people and chat.\nIf you need **assistance** you can contact staff in <#1274474625253773414>.}$v{thumbnail: {user.avatar}}$v{content: {user.mention}}$v{footer: We are now at {guild.count} members.}
1120434472114999307	1281076509838278710	welcome, {user.mention}!
1117506964155551814	1274875330947055657	{user.mention}, Welcome to SmartServices.
1258003767161389087	1276425377438367826	hello bitch read em rules like a good little bitch
1275204588894683247	1282388871434211419	{embed}$v{description: welcome to /pilot\n<#1275204744134266931> <#1275212833264500817> <#1277780890495483974> }$v{title: ★ }$v{content: Hey! Thanks for joining, {user.mention}!}$v{thumbnail: {user.avatar}}
1282466911870783518	1283686194500206624	{embed}$v{content: {user.mention}}$v{color: #5865f2}\nwould be: <@1194519294202101781>
1237392684113723423	1284610231443128390	{embed}$v{description: {embed}$v{description: Welcome to <a:flickerkos:1252440714927931492> \n★ <#1245871998425497694>\n★ <#1284603772072628308>\nRep /kos for pic perms}$v{thumbnail: {user.avatar}}$v{content: {user.mention}}}$v{color: #ffffff}
1121315810892316754	\N	{embed}$v{title: /gakko}$v{description: ty for joining /gakko! be active.}$v{color: #5865f2
1285074920627507210	\N	welcome to /all  rep /all in vanity for pic perms
1284829930726887465	1284831358622892074	Welcome {user.mention} to @wbu \n          Make sure to check <#1284834136351047783> \n                      .gg/wbu
1253955554334871632	1253955554334871635	{user.mention} welcome to {guild.name}
1281680936316178482	1286372804824141965	wlc to {guild.vanity} {user.mention}, stay active!
1285074886582206484	\N	{user.mention} sup
1274454080286232617	1283559647852232746	,ce {embed}$v{content: {user.mention}}$v{description: welcome, **{user.name}**\n[rules](https://discord.com/channels/1274454080286232617/1274454080286232622)\n[boosts](https://discord.com/channels/1274454080286232617/1279859917624180807)\n[voice](https://discord.com/channels/1274454080286232617/1277728053937574000)}$v{thumbnail: {user.avatar}}$v{footer: {guild.count} @ {guild.vanity}}
1287533179166523432	1293015950412746845	\N
1287161213502881874	1287201565417144476	{embed}$v{content: {user.mention}}$v{author: welc to /lie #invites 🦇 && {guild.icon} }$v{description: <:0000quote:1287200385202917426> Read the [rules](https://discord.com/channels/1287161213502881874/1287165077107118164)\n<:0000quote:1287200385202917426> be active in [chat](https://discord.com/channels/1287161213502881874/1287166874991202355)\n<:0000quote:1287200385202917426> view the ancs in [psa](https://discord.com/channels/1287161213502881874/1287165230681559236)}$v{color: #000000}$v{thumbnail: {user.avatar} }
1289741574552424518	1289741575223640256	\N
1279185435297452063	1283452990409150516	{embed}$v{description: **welcome to Arrive 📲**\n > • [/arrive](https://discord.gg/arrive)\n> • main us & <a:boosting:1291537557535850538> for pic and perms .\n> • mass dm and inv fgs for perms <:annc:1291538930910494775>}$v{footer: {guild.count} members | {guild.boost_count} boosts}$v{content: {user.mention}}
1232760919113863279	\N	wsp {usermention}
1288186497585123340	1288528431193133158	wys {user.mention}
1283124591048527892	1290598632575209568	yo welcome to /shooting <:blue_thumbs_up:1158065171852427294>
1260827368625279159	1285720213773619211	**sup {user.mention}**
1291976014540570624	1292607861754564618	welcome to the sever boost and rep for perms!
1227007783602491423	\N	wlc {user.mention}
1286694780121911347	\N	welcome {user.mention} to offroxys#SWS rep /offroxys for pics
1267301925813223434	1289049245818556426	hi! {user.mention}
1244403114447212564	1293964677109518478	sup {user.mention}
1284193880379625482	\N	welcome {user_mention}
1285735874566553631	1294796348406894652	*welc {user.mention}* <a:00001_nf2u:1286879945284648972>
1294870137903517737	1294870138432131135	dm <@929503912728334407> 4 access {user.mention}<:steambored:1265785956930420836>
1285311979057319976	1295477215261233183	sup {user.mention}
1295584203081252884	1295589604946219051	{embed}{timestamp: true}$v{title: Welcome to Tricks}$v{content: {user.mention}}$v{description: Be sure to read our rules here<#1295585392875274290>\n\n**Enjoy your time here.** \n\n**Need support? [Click Here](https://discord.com/channels/1295584203081252884/1295588701425897512)**}$v{color: #787878}
1295531878563971134	1295532247717253171	{user.mention} welcome to JaysShop feel free to <#1295532254759620700> and ask for prices and what we offer! <:shoppingcart:1295629471507808277>
1151241272326099056	1295751276046585937	Welcome to Midnight Agency | RR! 🥳
1292430925141119037	1295827456766513305	welcome {user.mention} to {guild.name} <:OrangePumpkin:1292547187028398225>
1293699972172091523	1296893095350370436	welc {user.mention} rep /remains for pic perms
1295649687453438033	1295716401277046876	welcome to xioshop {user.mention} make sure to check out <#1295714360190046248> , and <#1296722377132216341>
1297293375204229120	1297295965631414283	hi {user.mention}
1212420500366557264	1264507331811479572	{\n  "content": "",\n  "tts": false,\n  "embeds": [\n    {\n      "id": 664057046,\n      "description": "welcome {member.mention} ",\n      "fields": []\n    }\n  ],\n  "components": [],\n  "actions": {}\n}
1298398436638326836	1298398438328766475	**heyyy willkommen auf habibis** <:happy_blush:1298406703242678323>
1298807622484627530	1298813336032641047	{embed}{autodelete: 0.5}$v{&& icon: {guild.icon}}$v{title: @wonder}$v{content: {user.mention}}$v{description: <:bgwaveicon:1298828389091639366> **Welcome to** ***wonder***\n**<a:membericon:1298825890981220362>  [chat](https://discord.com/channels/1298807622484627530/1298813336032641047)\n<:voicechaticon:1298827226027917365>  [join vc](https://discord.com/channels/1298807622484627530/1298825176204578857)\n<:stafficon:1298826847575871568>  [support](https://discord.com/channels/1298807622484627530/1298812916312707153)**}$v{thumbnail: {user.avatar}}$v{color: #5a5a5a}$v{footer: we now have {guild.count} members}
1299477839103660052	1299507770005127392	{embed}{title: HI HI HI HI HI HI HI HI HI HI HI HI HI HI HI HI HI}$v{content: {user.mention} leave fn}$v{description: Reasons **WHY YOU SHOULD** Stay:\n1. Ok\n1. Ok\n1. Ok\n1. Ok\n1. Ok\n1. Ok\n1. Ok\n1. Ok\n1. Ok\n\n\n\n}
1183029663149334579	1286788956389904404	lol
1183029663149334579	1287128340897206343	{embed}$v{description: hi {user.mention}}
1291961786852970558	1300639257416831048	wsp {user.mention}
1291961786852970558	1300658806606528604	<a:1259847717161795636:1293815082345697290> {user.mention} check out <#1296927860426014781> <#1300643523670048778> <#1300639257416831048> that's all stay safe and main bounty !
1274569048205824153	1300554267886882816	welc {user.mention} to **/further** *boost & main 4 roles* <a:00:1300563468864327752> \n\n* [make a vc!](<https://discord.com/channels/1274569048205824153/1300971001781289051>) \n* talk and main <#1300554267886882816> \n* make sure to boost for awesome perms \n* dm <@1160907025434279976> to become a mod or admin <:000:1300563269387288607> \n\n## @further \ndnt spam/raid have fun in /further  <:000:1300563367232012311>
1274569048205824153	1300982101482541056	welc {user.mention} main & boost
1301221390388822038	1301223846610866288	enjoy {user.mention}
949837695050469456	1287442115898507405	{embed}$v{title: welc 2 {guild.vanity}}$v{description: ; read the rules\n; rep /shots in status\n; boost, invite & main us}$v{footer: boost or rep 4 pic perms}$v{thumbnail: {user.avatar}}$v{content: {user.mention}}
1119311424473276416	1301924053141160038	welc __{user.mention}__ <a:0051:1121400332753321984>
1302091501479919779	1302096316389916743	{user} Hello!
1296674979714170921	1302512323981869066	**welc {user.mention}!** rep & boost us for roles!
\.


--
-- Data for Name: channels; Type: TABLE DATA; Schema: voicemaster; Owner: postgres
--

COPY voicemaster.channels (guild_id, owner_id, channel_id) FROM stdin;
1075834904706826322	581745440534298624	1278803210018226178
1275204588894683247	1276597668365205588	1282406802788454461
1298459389220622368	1110031353510121482	1299223184028991508
1274164559296335922	1104828832919330816	1302620846854242346
1289741574552424518	1246491732992851968	1302633627980402754
\.


--
-- Data for Name: configuration; Type: TABLE DATA; Schema: voicemaster; Owner: postgres
--

COPY voicemaster.configuration (guild_id, channel_id, interface_id, category_id) FROM stdin;
1152334664153960509	1269940514652950581	1269940513587335246	1269940512635359232
1245364433065218098	1270338370450751565	1270338369431277610	1270338368546279510
1271295719843565589	1271830919875006578	1271830918721441803	1271830917358420120
1254044520467923034	1271830934382968924	1271830933615542292	1271830932508377143
1272020420760965140	1272046859774328842	1272046858176303188	1272046857513599006
1241483850622959797	1274509364924780625	1274509364287504468	1274509363490324671
1275486271736774668	1275490188641964094	1275490187983458314	1275490187333468221
1212420500366557264	1277741714085380217	1277741713095393333	1277741712122581054
1273202478468304998	1278309335914516512	1278309335537156126	1278309334614540360
1278101404141092895	1278488939946311712	1278488938838888541	1278488938327183431
1075834904706826322	1278782092087660647	1278782090686631949	1278782090086711419
1276605260110237758	1279033008292368497	1279033007562428466	1279033006337556540
1260459692426006550	1279615001425870911	1279615000167714887	1279614999391768576
1270486377460404356	1279981981253242889	1279981980515041352	1279981979760328775
1274295248255717477	1280105271229681746	1280105270160134257	1280105268809695272
1279205866993877085	1280642813901406260	1280642812618084507	1280642812022620285
1256851790540832831	1280977766086606920	1280977764756881520	1280977763536212031
1270864302877966436	1281484670508204084	1281484669636050984	1281484668973219840
1267058530175684759	1281689046862663680	1281689045654831167	1281689044270452758
1281680936316178482	1281691570424250543	1281691569564418140	1281691568826482810
1276302538152611972	1282108406412476468	1282108405728808960	1282108405061910641
1275204588894683247	1282341487836794890	1282341487123890329	1282341486234701824
1282466911870783518	1282819852255498252	1282819851840258139	1282819851206922341
1268557160284033107	1283465601133711365	1283465599741333544	1283465599070240859
1282717776112517291	1283715500152590387	1283715498999025705	1283715498164617239
1282393410204078141	1284045064846442587	1284045063394955298	1284045062350835836
1272301892776755210	1284354897805836320	1284354897092939836	1284354896405200916
1284475167703171114	1284481334101934101	1284481332143198291	1284481331044159500
1284532619383672853	1284535704763891743	1284535704197533907	1284535703337828463
1284756954933362688	1284759028341145663	1284759027473059881	1284759026516754476
1241058950145769482	1284898037768126484	1284898036778008619	1284898036304187413
1121315810892316754	1284938273122291723	1284938272400871424	1284938271209689202
1282926708650938410	1285009179181842492	1285009178431062046	1285009177181425748
1206215747869614122	1285228826066030633	1285228825117986867	1285228823864021022
1233306611074732082	1285272004592930879	1285272004005462088	1285272002697101419
1273027656933314600	1285341204900483072	1285341204120207451	1285341203285540874
1279499166954946591	1285674562322698351	1285674561324449924	1285674560846299218
1266853535887392841	1286221367720808511	1286221367091662898	1286221365644492920
1286345847126229053	1286500445832871966	1286500445086421002	1286500443748438018
1287161213502881874	1287164298057089097	1287164296693940298	1287164296291418124
1287215178399744041	1287430094507479102	1287430093588795392	1287430092363923487
949837695050469456	1287442339840655494	1287442338893004893	1287442338234237051
1274599092630061066	1287629571369336867	1287629569909587990	1287629569372721202
1283124591048527892	1287734675124785152	1287734674172411974	1287734673094606889
1264583661932777482	1287884941983748140	1287884941287358466	1287884940331188295
1288335344969711678	1288336368254058516	1288336367285174314	1288336366605701120
1284592876088463495	1288353981109768213	1288353979818049559	1288353978991771743
1260827368625279159	1288522596026945581	1288522594735095829	1288522593963606119
1288186497585123340	1289544376355131427	1289544375537504299	1289544375193567314
1286694780121911347	1289959161127501845	1289959160020078602	1289959158640148576
1289741574552424518	1290169015129341983	1290169013850083368	1290169012940177490
1288119126602285197	1291599009739313152	1291599008460177439	1291599007914922097
1292499075912171673	1292841678175997987	1292841677496782889	1292841676783620159
1291992395927523448	1293271009914261627	1293271009172131930	1293271007108403271
1292785447529087067	1293300354590572554	1293300353667698740	1293300352426446930
1286838746888536075	1293420827227852861	1293420826028150795	1293420825323634828
1284579437152702587	1293578560120033300	1293578558933041225	1293578557888401430
1293699972172091523	1293711933891153930	1293711932913745942	1293711931646935122
1283713863589564457	1293909616987471966	1293909615783972885	1293909615158755388
1070762079985877102	1293940633572216896	1293940632490086532	1293940631319744615
1287951817971339288	1294028502311370795	1294028501552336926	1294028500214480960
1232760919113863279	1294138351653486624	1294138350621687839	1294138350076301312
1285735874566553631	1294367954565337170	1294367953222897665	1294367952484958258
1284193880379625482	1294467296361840751	1294467295325978683	1294467294457761834
1292985929954365472	1294555354612371527	1294555353232441408	1294555351605051494
1287533179166523432	1295102123532619817	1295102122257285271	1295102121452240918
1244724607584436244	1295103640348131418	1295103639399960647	1295103638645112966
1295105048161812540	1295114592770592773	1295114591654904032	1295114590098554982
1294870137903517737	1295126236971925626	1295126235986399312	1295126235118305351
1268317659037171833	1295447495668793374	1295447494821679166	1295447494083346532
1285311979057319976	1295469916849180805	1295469916174024828	1295469914974457897
1151241272326099056	1295566931339776091	1295566929863376997	1295566928584118312
1294660772361666603	1296882074082349077	1296882072920526982	1296882072035524678
1297293375204229120	1297396643632517150	1297396642827206676	1297396641766183006
1121045839012438027	1297677096876773426	1297677095736053870	1297677094490472660
1298398436638326836	1298412817506107463	1298412816365256725	1298412815719333910
1298807622484627530	1298825176204578857	1298825175264919664	1298825174795292693
1298459389220622368	1298856810840588319	1298856809599209524	1298856808903082100
1274781210475892756	1299347415589064706	1299347415039610931	1299347414112800821
1295820951388422226	1299811895733125121	1299811895384997988	1299811894646931538
1283233718592606311	1299959006403760218	1299959005766225972	1299959004692348970
1291961786852970558	1300665144182833152	1300665143272935537	1300665142459236352
1274569048205824153	1300971001781289051	1300970999919149101	1300970999059316827
1236667753755181068	1301828926842208308	1301828926015930402	1301828925508550666
1119311424473276416	1301935638580564039	1301935637850493098	1301935636638466189
1244403114447212564	1301981845449085100	1301981844287262771	1301981843851051100
1302091501479919779	1302110357376073809	1302110356499337267	1302110355656409190
1299875586147225610	1302427694767800420	1302427693761036339	1302427693324697680
1234621599420776550	1302429683870339174	1302429682981015605	1302429682725294100
1274164559296335922	1302435787060678676	1302435785957703762	1302435785147945074
1296674979714170921	1302499751148650496	1302499750180028416	1302499749194240002
\.


--
-- Name: api_key_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.api_key_id_seq', 5, true);


--
-- Name: afk afk_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.afk
    ADD CONSTRAINT afk_pkey PRIMARY KEY (user_id);


--
-- Name: api_key api_key_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_key
    ADD CONSTRAINT api_key_key_key UNIQUE (key);


--
-- Name: api_key api_key_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_key
    ADD CONSTRAINT api_key_pkey PRIMARY KEY (id);


--
-- Name: api_key api_key_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.api_key
    ADD CONSTRAINT api_key_user_id_key UNIQUE (user_id);


--
-- Name: authed authed_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authed
    ADD CONSTRAINT authed_pkey PRIMARY KEY (guild_id);


--
-- Name: autoresponder autoresponder_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autoresponder
    ADD CONSTRAINT autoresponder_pkey PRIMARY KEY (guild_id, trigger);


--
-- Name: autorole autorole_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autorole
    ADD CONSTRAINT autorole_pkey PRIMARY KEY (guild_id);


--
-- Name: blacklist blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blacklist
    ADD CONSTRAINT blacklist_pkey PRIMARY KEY (user_id);


--
-- Name: blacklistguild blacklistguild_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.blacklistguild
    ADD CONSTRAINT blacklistguild_pkey PRIMARY KEY (guild_id);


--
-- Name: boostmessage boostmessage_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.boostmessage
    ADD CONSTRAINT boostmessage_pkey PRIMARY KEY (guild_id);


--
-- Name: br_award br_award_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.br_award
    ADD CONSTRAINT br_award_pkey PRIMARY KEY (guild_id, role_id);


--
-- Name: cases cases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases
    ADD CONSTRAINT cases_pkey PRIMARY KEY (guild_id);


--
-- Name: chatbot chatbot_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.chatbot
    ADD CONSTRAINT chatbot_pkey PRIMARY KEY (guild_id);


--
-- Name: counters counters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.counters
    ADD CONSTRAINT counters_pkey PRIMARY KEY (guild_id);


--
-- Name: disablecommand disablecommand_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.disablecommand
    ADD CONSTRAINT disablecommand_pkey PRIMARY KEY (guild_id, command);


--
-- Name: economy economy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.economy
    ADD CONSTRAINT economy_pkey PRIMARY KEY (user_id);


--
-- Name: filter filter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.filter
    ADD CONSTRAINT filter_pkey PRIMARY KEY (guild_id, mode);


--
-- Name: forcenick forcenick_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.forcenick
    ADD CONSTRAINT forcenick_pkey PRIMARY KEY (guild_id, user_id);


--
-- Name: guild_settings guild_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guild_settings
    ADD CONSTRAINT guild_settings_pkey PRIMARY KEY (guild_id);


--
-- Name: guilds guilds_guild_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.guilds
    ADD CONSTRAINT guilds_guild_id_key UNIQUE (guild_id);


--
-- Name: invoke invoke_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.invoke
    ADD CONSTRAINT invoke_pkey PRIMARY KEY (guild_id, type);


--
-- Name: joindm joindm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.joindm
    ADD CONSTRAINT joindm_pkey PRIMARY KEY (guild_id);


--
-- Name: joinping joinping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.joinping
    ADD CONSTRAINT joinping_pkey PRIMARY KEY (guild_id, channel_id);


--
-- Name: lastfm lastfm_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lastfm
    ADD CONSTRAINT lastfm_pkey PRIMARY KEY (user_id);


--
-- Name: levels levels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.levels
    ADD CONSTRAINT levels_pkey PRIMARY KEY (user_id);


--
-- Name: logging logging_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logging
    ADD CONSTRAINT logging_pkey PRIMARY KEY (guild_id);


--
-- Name: modlogs modlogs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.modlogs
    ADD CONSTRAINT modlogs_pkey PRIMARY KEY (guild_id);


--
-- Name: names names_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.names
    ADD CONSTRAINT names_pkey PRIMARY KEY (user_id);


--
-- Name: premium premium_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.premium
    ADD CONSTRAINT premium_pkey PRIMARY KEY (user_id);


--
-- Name: restore restore_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restore
    ADD CONSTRAINT restore_pkey PRIMARY KEY (guild_id, user_id);


--
-- Name: restricted_words restricted_words_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.restricted_words
    ADD CONSTRAINT restricted_words_pkey PRIMARY KEY (guild_id, word);


--
-- Name: selfprefix selfprefix_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.selfprefix
    ADD CONSTRAINT selfprefix_pkey PRIMARY KEY (user_id);


--
-- Name: starboard starboard_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.starboard
    ADD CONSTRAINT starboard_pkey PRIMARY KEY (guild_id);


--
-- Name: timezones timezones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.timezones
    ADD CONSTRAINT timezones_pkey PRIMARY KEY (user_id);


--
-- Name: topcmds topcmds_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.topcmds
    ADD CONSTRAINT topcmds_pkey PRIMARY KEY (command_name);


--
-- Name: usertracker usertracker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usertracker
    ADD CONSTRAINT usertracker_pkey PRIMARY KEY (guild_id);


--
-- Name: vanityroles vanityroles_channel_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vanityroles
    ADD CONSTRAINT vanityroles_channel_id_key UNIQUE (channel_id);


--
-- Name: vanityroles vanityroles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vanityroles
    ADD CONSTRAINT vanityroles_pkey PRIMARY KEY (guild_id);


--
-- Name: vanityroles vanityroles_role_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vanityroles
    ADD CONSTRAINT vanityroles_role_id_key UNIQUE (role_id);


--
-- Name: vanitytracker vanitytracker_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vanitytracker
    ADD CONSTRAINT vanitytracker_pkey PRIMARY KEY (guild_id);


--
-- Name: vape vape_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vape
    ADD CONSTRAINT vape_pkey PRIMARY KEY (user_id);


--
-- Name: vc_stats vc_stats_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vc_stats
    ADD CONSTRAINT vc_stats_pkey PRIMARY KEY (user_id);


--
-- Name: channels channels_channel_id_key; Type: CONSTRAINT; Schema: voicemaster; Owner: postgres
--

ALTER TABLE ONLY voicemaster.channels
    ADD CONSTRAINT channels_channel_id_key UNIQUE (channel_id);


--
-- Name: configuration configuration_category_id_key; Type: CONSTRAINT; Schema: voicemaster; Owner: postgres
--

ALTER TABLE ONLY voicemaster.configuration
    ADD CONSTRAINT configuration_category_id_key UNIQUE (category_id);


--
-- Name: configuration configuration_channel_id_key; Type: CONSTRAINT; Schema: voicemaster; Owner: postgres
--

ALTER TABLE ONLY voicemaster.configuration
    ADD CONSTRAINT configuration_channel_id_key UNIQUE (channel_id);


--
-- Name: configuration configuration_guild_id_key; Type: CONSTRAINT; Schema: voicemaster; Owner: postgres
--

ALTER TABLE ONLY voicemaster.configuration
    ADD CONSTRAINT configuration_guild_id_key UNIQUE (guild_id);


--
-- Name: configuration configuration_interface_id_key; Type: CONSTRAINT; Schema: voicemaster; Owner: postgres
--

ALTER TABLE ONLY voicemaster.configuration
    ADD CONSTRAINT configuration_interface_id_key UNIQUE (interface_id);


--
-- PostgreSQL database dump complete
--

