import { createQueryClient } from "@shared/lib/query-client";
import { cache } from "react";
import "server-only";

export const getQueryClient = cache(createQueryClient);
