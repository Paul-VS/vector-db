create or replace function match_page_sections(embedding vector(1536), match_threshold float, match_count int, min_content_length int)
returns table (content text, similarity float)
language plpgsql
as $$
#variable_conflict use_variable
begin
  return query
  select    
    page_section.content,
    (page_section.embedding <#> embedding) * -1 as similarity
  from page_section
  -- We only care about sections that have a useful amount of content
  where length(page_section.content) >= min_content_length

  -- The dot product is negative because of a Postgres limitation, so we negate it
  and (page_section.embedding <#> embedding) * -1 > match_threshold

  -- OpenAI embeddings are normalized to length 1, so
  -- cosine similarity and dot product will produce the same results.
  -- Using dot product which can be computed slightly faster.
  --
  -- For the different syntaxes, see https://github.com/pgvector/pgvector
  order by page_section.embedding <#> embedding
  
  limit match_count;
end;
$$;