#include "vma.h"

arena_t *alloc_arena(const uint64_t size)
{
    return NULL;
}

void dealloc_arena(arena_t *arena)
{

}

void alloc_block(arena_t *arena, const uint64_t address, const uint64_t size)
{

}

void free_block(arena_t *arena, const uint64_t address)
{

}

void read(arena_t *arena, uint64_t address, uint64_t size)
{

}

void write(arena_t *arena, const uint64_t address, const uint64_t size, int8_t *data)
{

}

void pmap(const arena_t *arena)
{

}

void mprotect(arena_t *arena, uint64_t address, int8_t *permission)
{

}