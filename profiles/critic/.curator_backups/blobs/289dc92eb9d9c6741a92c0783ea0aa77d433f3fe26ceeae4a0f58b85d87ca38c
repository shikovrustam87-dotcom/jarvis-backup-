---
name: kabardian-genealogy-research
description: "Research Kabardian family trees via zolka.ru archives."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [genealogy, kabardian, circassian, kbr, archives, family-tree, north-caucasus]
    related_skills: [blocked-page-recovery, grounded-citations]
---

# Kabardian Genealogy Research

## When to Use

- User asks to find ancestors, family tree, or genealogy of a Kabardian (or
  North Caucasian) family.
- User mentions a surname and village from KBR and wants to trace lineage.
- User asks about historical records, household lists, or archive documents
  for a North Caucasian family.

How to research family trees of Kabardian (and other North Caucasian) families,
primarily from Kabardino-Balkaria (KBR). The user is Kabardian, Muslim, from
Shalushka village, Chegem district — but the techniques apply to any KBR family.

## Primary sources (in order of usefulness)

1. **zolka.ru** — the single most valuable source. Contains:
   - Household lists (подворные списки) by village and year (1862, 1905, 1926, etc.)
   - The book "Генеалогия кабардинских фамилий" (Бейтуганов, 2009) — 950 pages,
     family genealogies with page numbers in the alphabetical index
   - Lists of disenfranchised persons (списки лишенцев) by village
   - Metrical books (метрические книги)
   - Genealogy articles and DNA-genealogy data
   - Search: `site:zolka.ru "<surname>" "<village>"`

2. **KBR archive (arhiv.kbr.ru)** — official archive of KBR. May be IP-blocked;
   if blocked, try from a different network or VPN.

3. **KBR municipal sites** (chegem.kbr.ru, etc.) — village administration pages,
   sometimes contain historical documents.

4. **Social media / forums** — VK groups for KBR villages, genealogy forums.
   Search: `"<surname>" "<village>" site:vk.com`

## Research procedure

### Step 0: User preference — keep searching, don't ask

When the user says "не спрашивай, ищи пока не найдёшь до основателя рода" or similar,
do NOT ask "should I continue?" or "is this enough?" at each step. Keep searching through
all available sources until you either find the clan founder or exhaust all digitized
sources. Only present a summary when you've hit the bottom of available records.

### Step 1: Identify the village and surname

Ask the user for:
- Full name of the person (in Russian and/or Kabardian form)
- Village of origin (селение)
- District (район) if known
- Approximate birth year
- Father's name (отчество) if known
- Spouse's name if known (especially mixed marriages — wives' names are rarely
  recorded in old documents, so this is a strong differentiator)
- **If the user is speaking (voice input):** ask them to spell each name slowly.
  Kabardian names are frequently misrecognized by Russian STT (Темиркан →
  «Тамиш», Нарт → «Нав»). Confirm spellings before searching — a wrong name
  compounds into a wrong tree.

### Step 2: Search zolka.ru for household lists

Search for the village's household lists:
- `site:zolka.ru "<village>" подворный список` or `посемейный список`
- Look for lists from 1862, 1886, 1905, 1926 — these are the most common years
- The 1905 lists are the most detailed: head of household, age, sons with ages,
  count of females ("женского пола")

### Step 2b: Cross-village search when family not found in target village

If the family is NOT found in the target village's records for a given year:
- Check neighboring villages and auls in the same district
- Families frequently moved between villages (especially between 1862 and 1905)
- Search `site:zolka.ru "<surname>" "<neighboring village>" <year>`
- Example: Шиковы were NOT in 1862 Shalushka but WERE in 1862 Karmovo (с. Каменномостское).
  They moved to Shalushka between 1862 and 1905.

### Step 3: Match the person in the list

In the 1905 lists, entries look like:
```
48. Шиков Цут Гулович — 70 лет. Сыновья: Жантемир — 18 лет, Мухамед — 12 лет,
Хамид — 3 года. Женского пола — 5
```

Match by:
- Surname + first name (may be spelled differently: Мухаммад/Магомед/Мухамед/Магомет)
- Age in the list year → birth year
- Father's name (отчество) → the head of household
- Siblings mentioned → cross-reference with user's knowledge
- Count of "женского пола" → number of females in household
- **Shared patronymic across multiple entries** → indicates common father. Group
  all entries with the same patronymic before matching individuals; ask the user
  if they know any of the siblings (e.g., "did your grandfather have an uncle
  named Батоко?")

### Step 4: Trace the lineage

**Upward (ancestors):** If matched, the head of household is the father. Repeat
the search for the father's name in earlier lists (1862, 1886) to go further back.

**Downward (descendants):** When the person of interest was born AFTER the
available records, work forward. The 1905 list's children born ~1890-1905 are
potential fathers of people born ~1910-1925, who are potential fathers of people
born ~1935-1945. Build a candidate table of all sons from the 1905 list with
birth years, then match by approximate age and sibling patterns. Cross-check
with the user's knowledge of children's names and spouse's name.

### Step 5: Check the genealogy book

Search zolka.ru for "Генеалогия кабардинских фамилий" + surname:
- `site:zolka.ru "<surname>" генеалогия кабардинских фамилий`
- The alphabetical index gives page numbers (e.g., "Шиков 210, 416")
- The book itself may not be freely available online — note the pages for the user

### Step 6: Check disenfranchised lists

Search for "список лишенцев" + village name on zolka.ru.
These lists (1930) contain names, birth years, and reasons for disenfranchisement.
Useful for confirming individuals from the 1905 lists who were still alive in 1930.

### Step 7: Cross-reference and present findings

Present findings as a family tree with:
- Confirmed matches (high confidence)
- Possible matches (need user confirmation)
- Open questions (what additional info would help)

## Confirmed family trees

### Шиков (Shikov) — село Шалушка, Чегемский район

**Родовое древо (подтверждено по архивам 1905 г.):**
- Хацу (Хакуц) — прапрапрадед (имя не найдено в digitized источниках)
- Шиков Уготыж Хацуевич — прапрадед (род. ~1847, 58 лет в 1905 г.)
- Шиков Тимиркан Уготыжевич — прадед (род. ~1882, 23 года в 1905 г.)
- Шиков Мухаммад Тимирканович — дед (род. 1932)
  - Жена: Катя (Екатерина)
  - Дети (7): Сауди, Муаед, Вячеслав, Валера, Лариса, Антиса, Анжела

**Братья Уготыжа (сыновья Хацу):**
- Хакуц Хацуевич (род. ~1870) — сыновья: Сагатгирей, Моухож
- Батоко Хацуевич (род. ~1860) — сыновья: Саид, Мурат, Узеир
- Аслануко Хацуевич (род. ~1858) — сын: Шамсадин

**Источник:** Подворный семейный список селения Шалушка, Нальчикского округа, 1905 г. (zolka.ru)

**Дополнительно (1862 г.):** Шиковы НЕ найдены в 1862 Шалушке (аул Шарданова), но найдены в 1862 Кармово (с. Каменномостское): "Пшкан Шиков" и "пасынок Пшикана Шиковы". Семья переехала в Шалушку между 1862 и 1905 гг.

## Key pitfalls

1. **Name spelling variations.** Kabardian names are transliterated differently across
   documents: Мухаммад/Магомед/Мухамед/Магомет, Жантемир/Джантемир, Хамид/Хамит.
   Always search for multiple spellings.

2. **Multiple families with the same surname in one village.** In Shalushka alone there
   were 11 Шиков families in 1905. Don't assume the first match is correct — cross-check
   with age, father's name, and siblings.

3. **Women's names not recorded.** Old lists only count "женского пола" (females).
   If the user knows a wife's name (especially a Russian name like Катя/Екатерина),
   this is a strong differentiator for mixed marriages — note it prominently.

4. **KBR archive may be IP-blocked.** arhiv.kbr.ru sometimes returns 403. Don't
   treat this as "no data exists" — try alternate access methods.

5. **Age ≠ exact birth year.** Ages in lists are often approximate (rounded to
   nearest 5 or 10). A person listed as "12 лет" in 1905 could be born in 1892-1894.

6. **Don't confuse similar surnames.** Шиков vs Шихов vs Шахов — different families.
   Always verify the exact spelling in the source document.

7. **Present uncertain matches as questions, not facts.** Ask the user to confirm
   before building the family tree. Wrong matches compound into wrong trees.

8. **Search engine snippets as fallback for truncated pages.** When web_extract truncates
   the middle of a long page (e.g., a 15,000-character household list), the search
   engine snippets from web_search can still show the specific entries. Search for
   `site:zolka.ru "<surname>" "<village>"` — the snippets often contain the exact
   lines you need even when the full page extraction omits them.

9. **Multi-generation tracing.** When the person of interest was born after the
   available records (e.g., born 1939 but only 1905 lists exist), work backwards:
   the 1905 list's children born ~1890-1905 are potential fathers of people born
   ~1910-1925, who are potential fathers of people born ~1935-1945. Build a
   candidate table of all sons from the 1905 list with birth years, then match
   by approximate age and sibling patterns.

10. **"Not found" ≠ "doesn't exist."** A person not found in digitized sources may
    still exist in non-digitized archives (KBR archive, metrical books, census
    records). Always present "not found online" as "not found in digitized sources"
    and recommend contacting the KBR archive or checking non-digitized records.
    Never imply the person or family doesn't exist.

11. **Voice recognition corrupts Kabardian names.** When the user communicates
    by voice (Russian STT), Kabardian names are often misrecognized: Темиркан →
    «Тамиш», Нарт → «Нав», «Дед мой» → «Джарис Матри». Always ask the user to
    confirm the exact spelling of each name before building the tree. When a name
    doesn't match any archive entry, try common Kabardian phonetic variants and
    present them as candidates for the user to confirm — never guess which one is
    correct.

12. **Shared patronymic = shared father.** In 1905 lists, multiple entries with
    the same patronymic (e.g., four "Хацуевич" brothers: Хакуц, Батоко,
    Аслануко, Уготыж) indicate a common father. This is a strong clustering
    signal — group siblings before matching individuals, and use the sibling set
    to cross-check the user's family knowledge (e.g., "did your grandfather have
    an uncle named Батоко?").

13. **Confirm names before presenting the tree.** When working from voice input,
    present candidate matches as questions ("could this be Темиркан?") rather than
    facts. Only mark a match as confirmed after the user explicitly confirms the
    spelling. Voice-garbled names compound into wrong trees if assumed correct.

14. **Cross-village search.** When a family is NOT found in the target village's records
    for a given year, don't conclude they didn't exist — check neighboring villages and
    auls in the same district. Families frequently moved between villages (especially
    between 1862 and 1905). Example: Шиковы were not in 1862 Shalushka but were found
    in 1862 Karmovo (с. Каменномостское).

## Output format

Present findings in Russian, structured as:
- Confirmed matches (высокая уверенность)
- Possible matches (требуется подтверждение)
- Open questions (что поможет уточнить)
- Next steps (что искать дальше)

Include the source document name and year for each finding.
