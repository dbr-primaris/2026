# באג ודאי — הקשר לפגישה (יולי 2026)

## הסימפטום שראינו
- שלב 1 מציג "3 נבחרו, מתוכם 4 ודאי" — בלתי אפשרי (ודאי > שריון)
- שלב 2 לא מציג ודאי בצבע זהב, ולא חוסם הסרה
- יש ודאי שאינו מסומן כלל בשלב 2

## הסיבה השורשית
`state.vadai` ו-`state.shiryun` יוצאים מסנכרון כשמנווטים הלוך-חזור בין השלבים.

**הנקודה הקריטית:** בכל מקום שמסיר מועמד מ-`shiryun` בשלב 2,  
הוא **לא** מסיר אותו גם מ-`vadai`. 

## כל נקודות השינוי שצריך לתקן

### state.html — 3 פונקציות שצריכות תיקון:

1. **`togglePick(name)`** — כשמסיר: מסיר מ-selected ו-shiryun, **לא** מ-vadai
2. **`toggleShiryunState(name)`** — כשמסיר שריון: מסיר מ-shiryun, **לא** מ-vadai  
3. **`toggleSquadPick(name)`** — callback הסרה: מסיר מ-selected ו-shiryun, **לא** מ-vadai

### process.html — שיקול:
4. **`resetAllSelections()`** — מסיר shiryun/selected/dbr_picks, משאיר vadai — שאלה: האם לאפס גם vadai?

### shiryun.html — כבר תקין:
- `cycleSelection()` — מוסיף/מסיר מ-vadai + shiryun ✓
- `toggleShiryun()` — מסיר גם מ-vadai כשמבטל שריון ✓

## תיקון הנוסחה

בכל הסרה מ-shiryun בשלב 2, להוסיף:
```js
state.vadai = (state.vadai || []).filter(x => x !== name);
```

## בעיית הקריאה — עדיין לא פתורה
גם לאחר תיקון ה-write, יש בעיית **read**: state.html לפעמים לא קורא state.vadai נכון.
הוספנו `console.log('[DBR vadai]', ...)` ב-renderRanking — לפתוח DevTools בשלב 2 כדי לראות מה יש בפועל.

## מה כבר נעשה (שינויים בשלב 2)
- `allPicks` כולל עכשיו גם `state.vadai`
- CSS עם `!important` לצבע זהב על `[data-vadai="1"]`
- onclick על שורות ודאי מחסים ישירות ל-toast (לא דרך togglePick)

## צעד הבא
סקירה מסודרת של כל מסלולי השינוי → תיקון עקבי ב-3 הפונקציות בstate.html + ודא שloadState מחזיר vadai תמיד.
