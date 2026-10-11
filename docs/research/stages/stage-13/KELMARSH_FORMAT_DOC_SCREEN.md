# Kelmarsh v4 official format-document screen

Status: **DEC-108 one-page owner-record screen completed; Director finding,
independent document QA pending; Stage 13 HOLD**. Accessed 2026-10-11.
The approved limit was at most two owner documentation pages. Only the known
[official Cubico Kelmarsh v4 record](https://zenodo.org/records/16807551)
was opened. No eligible linked owner format-document page was present, so a
second page was not opened.

The record describes ten-minute SCADA/events data from six turbines grouped
by year, notes variable signal availability, and lists a mapping from primary
SCADA to CSV signal names. It states Cubico's CC BY 4.0 release. It links to
the mapping CSV, static CSV and annual ZIPs as **data files**, plus general
corporate/contact links. It gives **no explicit delimiter, quote/encoding or
first-line/header rule** for the annual turbine-data CSVs. Searches within
this same page for `delimiter` and `header` returned no match. The record's
CSV mapping reference does not define the member-file dialect.

Result: annual member delimiter and header identity remain **unverified**.
DEC-107's one comma-delimited first-line field cannot be reinterpreted as one
channel, an alternative delimiter, or a malformed dataset from this page.
There was no ZIP/member/CSV preview, download, measurement, model score,
test/Electricity access or contact with the publisher. The approved two-page
ceiling was not used to browse a generic corporate site or an unrelated
dataset. DEC-108 is exhausted under its stop-if-unclear rule.

To resolve the dialect would require a separately approved source-file
audit or a new, specifically identified owner format document. Neither is
automatic. Source admission, formal role/split, concurrent finite channel
coverage, protocol/budget freeze and Stage 14 remain `HOLD`; H-04 is `not
tested` and DEC-070 public release `STOP` persists.
