# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: testProtocolCode.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='testProtocolCode.proto',
  package='',
  syntax='proto2',
  serialized_options=b'\n$com.janlr.ag.test.common.fixed.protoB\020testProtocolCodeH\003',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16testProtocolCode.proto*E\n\x08testGame\x12\x1a\n\x15TEST_AUTH_LOGIN_CHECK\x10\xe9\x07\x12\x1d\n\x18TEST_GT_PLAYER_HEARTBEAT\x10\xea\x07\x42:\n$com.janlr.ag.test.common.fixed.protoB\x10testProtocolCodeH\x03'
)

_TESTGAME = _descriptor.EnumDescriptor(
  name='testGame',
  full_name='testGame',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TEST_AUTH_LOGIN_CHECK', index=0, number=1001,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TEST_GT_PLAYER_HEARTBEAT', index=1, number=1002,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=26,
  serialized_end=95,
)
_sym_db.RegisterEnumDescriptor(_TESTGAME)

testGame = enum_type_wrapper.EnumTypeWrapper(_TESTGAME)
TEST_AUTH_LOGIN_CHECK = 1001
TEST_GT_PLAYER_HEARTBEAT = 1002


DESCRIPTOR.enum_types_by_name['testGame'] = _TESTGAME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
