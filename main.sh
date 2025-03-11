#!/bin/bash
exec poetry -C "$(dirname "${0}")" run test
