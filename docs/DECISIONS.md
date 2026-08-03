# Architekturentscheidungen

## ADR-001 – SQLite als Datenbank

### Entscheidung
SQLite wird in der ersten Projektversion als persistente Datenbank verwendet.

### Begründung
- geringer Einrichtungsaufwand
- Fokus auf Softwarearchitektur und ML
- keine externe Infrastruktur notwendig
- späterer Wechsel auf PostgreSQL vorgesehen

### Konsequenzen
+ einfache Entwicklung
+ schnelle Tests
- eingeschränkte Skalierbarkeit