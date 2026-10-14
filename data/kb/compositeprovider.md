# CompositeProvider

## Purpose
A CompositeProvider combines data from several providers with a union or a join. It is the usual object to expose data to queries in BW/4HANA.

## Union and join
A union stacks rows from several aDSOs that share the same characteristics. A join links two providers on matching fields and can return fewer rows if keys do not match.

## Performance notes
Joins on large providers cost more than unions. Keep join fields indexed by using characteristics with master data and avoid joining two very large transaction providers when a union is enough.
