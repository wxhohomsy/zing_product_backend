# Containment Logic

This document outlines the containment logic and object inheritance structure within our system. The inheritance hierarchy is critical for understanding the relationships between different entities.

## Object Inheritance Hierarchy

The inheritance structure is defined as follows:

- `Ingot`
  - `GrowingSegment`
    - `WaferingSegment`
      - `Lot`
        - `SublotLot`

### Detailed Relationships

- **Ingot to Growing Segment**: The relationship between an ingot and its growing segments is determined by the table `mesmgr.CGRWCONCRP`.
- **Growing Segment to Wafering Segment**: The wafering segment associated with a growing segment is also defined in `mesmgr.CGRWCONCRP`.
- **Segment to Sublot**: The sublot associated with a segment is determined by the table `mesmgr.mwipsltsts`.
- **Lot and Segment Association**: The association between a lot and a segment is established based on the presence of common sublots (mwipsltsts) between them.
