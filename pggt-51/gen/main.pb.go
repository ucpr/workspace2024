// Code generated by protoc-gen-go. DO NOT EDIT.
// versions:
// 	protoc-gen-go v1.34.2
// 	protoc        (unknown)
// source: main.proto

package gen

import (
	_ "github.com/srikrsna/protoc-gen-gotag/tagger"
	protoreflect "google.golang.org/protobuf/reflect/protoreflect"
	protoimpl "google.golang.org/protobuf/runtime/protoimpl"
	reflect "reflect"
	sync "sync"
)

const (
	// Verify that this generated code is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(20 - protoimpl.MinVersion)
	// Verify that runtime/protoimpl is sufficiently up-to-date.
	_ = protoimpl.EnforceVersion(protoimpl.MaxVersion - 20)
)

type Example struct {
	state         protoimpl.MessageState
	sizeCache     protoimpl.SizeCache
	unknownFields protoimpl.UnknownFields

	A string `protobuf:"bytes,1,opt,name=a,proto3" json:"a,omitempty" a:"a" b:"a" bun:"a" bundle:"a" c:"a" csv:"a" d:"a" e:"a" f:"a" g:"a" h:"a" i:"a" pg:"a" yaml:"a"`
	B string `protobuf:"bytes,2,opt,name=b,proto3" json:"b,omitempty" a:"b" b:"b" bun:"b" bundle:"b" c:"b" csv:"b" d:"b" e:"b" f:"b" g:"b" h:"b" i:"b" pg:"b" yaml:"b"`
	C string `protobuf:"bytes,3,opt,name=c,proto3" json:"c,omitempty" a:"c" b:"c" bun:"c" bundle:"c" c:"c" csv:"c" d:"c" e:"c" f:"c" g:"c" h:"c" i:"c" pg:"c" yaml:"c"`
}

func (x *Example) Reset() {
	*x = Example{}
	if protoimpl.UnsafeEnabled {
		mi := &file_main_proto_msgTypes[0]
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		ms.StoreMessageInfo(mi)
	}
}

func (x *Example) String() string {
	return protoimpl.X.MessageStringOf(x)
}

func (*Example) ProtoMessage() {}

func (x *Example) ProtoReflect() protoreflect.Message {
	mi := &file_main_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms := protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}

// Deprecated: Use Example.ProtoReflect.Descriptor instead.
func (*Example) Descriptor() ([]byte, []int) {
	return file_main_proto_rawDescGZIP(), []int{0}
}

func (x *Example) GetA() string {
	if x != nil {
		return x.A
	}
	return ""
}

func (x *Example) GetB() string {
	if x != nil {
		return x.B
	}
	return ""
}

func (x *Example) GetC() string {
	if x != nil {
		return x.C
	}
	return ""
}

var File_main_proto protoreflect.FileDescriptor

var file_main_proto_rawDesc = []byte{
	0x0a, 0x0a, 0x6d, 0x61, 0x69, 0x6e, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x12, 0x07, 0x65, 0x78,
	0x61, 0x6d, 0x70, 0x6c, 0x65, 0x1a, 0x13, 0x74, 0x61, 0x67, 0x67, 0x65, 0x72, 0x2f, 0x74, 0x61,
	0x67, 0x67, 0x65, 0x72, 0x2e, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x22, 0xe8, 0x02, 0x0a, 0x07, 0x45,
	0x78, 0x61, 0x6d, 0x70, 0x6c, 0x65, 0x12, 0x73, 0x0a, 0x01, 0x61, 0x18, 0x01, 0x20, 0x01, 0x28,
	0x09, 0x42, 0x65, 0x9a, 0x84, 0x9e, 0x03, 0x60, 0x61, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x62, 0x3a,
	0x22, 0x61, 0x22, 0x20, 0x63, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x64, 0x3a, 0x22, 0x61, 0x22, 0x20,
	0x65, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x66, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x67, 0x3a, 0x22, 0x61,
	0x22, 0x20, 0x68, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x69, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x79, 0x61,
	0x6d, 0x6c, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x63, 0x73, 0x76, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x62,
	0x75, 0x6e, 0x64, 0x6c, 0x65, 0x3a, 0x22, 0x61, 0x22, 0x20, 0x62, 0x75, 0x6e, 0x3a, 0x22, 0x61,
	0x22, 0x20, 0x70, 0x67, 0x3a, 0x22, 0x61, 0x22, 0x52, 0x01, 0x61, 0x12, 0x73, 0x0a, 0x01, 0x62,
	0x18, 0x02, 0x20, 0x01, 0x28, 0x09, 0x42, 0x65, 0x9a, 0x84, 0x9e, 0x03, 0x60, 0x61, 0x3a, 0x22,
	0x62, 0x22, 0x20, 0x62, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x63, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x64,
	0x3a, 0x22, 0x62, 0x22, 0x20, 0x65, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x66, 0x3a, 0x22, 0x62, 0x22,
	0x20, 0x67, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x68, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x69, 0x3a, 0x22,
	0x62, 0x22, 0x20, 0x79, 0x61, 0x6d, 0x6c, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x63, 0x73, 0x76, 0x3a,
	0x22, 0x62, 0x22, 0x20, 0x62, 0x75, 0x6e, 0x64, 0x6c, 0x65, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x62,
	0x75, 0x6e, 0x3a, 0x22, 0x62, 0x22, 0x20, 0x70, 0x67, 0x3a, 0x22, 0x62, 0x22, 0x52, 0x01, 0x62,
	0x12, 0x73, 0x0a, 0x01, 0x63, 0x18, 0x03, 0x20, 0x01, 0x28, 0x09, 0x42, 0x65, 0x9a, 0x84, 0x9e,
	0x03, 0x60, 0x61, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x62, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x63, 0x3a,
	0x22, 0x63, 0x22, 0x20, 0x64, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x65, 0x3a, 0x22, 0x63, 0x22, 0x20,
	0x66, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x67, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x68, 0x3a, 0x22, 0x63,
	0x22, 0x20, 0x69, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x79, 0x61, 0x6d, 0x6c, 0x3a, 0x22, 0x63, 0x22,
	0x20, 0x63, 0x73, 0x76, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x62, 0x75, 0x6e, 0x64, 0x6c, 0x65, 0x3a,
	0x22, 0x63, 0x22, 0x20, 0x62, 0x75, 0x6e, 0x3a, 0x22, 0x63, 0x22, 0x20, 0x70, 0x67, 0x3a, 0x22,
	0x63, 0x22, 0x52, 0x01, 0x63, 0x42, 0x7f, 0x0a, 0x0b, 0x63, 0x6f, 0x6d, 0x2e, 0x65, 0x78, 0x61,
	0x6d, 0x70, 0x6c, 0x65, 0x42, 0x09, 0x4d, 0x61, 0x69, 0x6e, 0x50, 0x72, 0x6f, 0x74, 0x6f, 0x50,
	0x01, 0x5a, 0x29, 0x67, 0x69, 0x74, 0x68, 0x75, 0x62, 0x2e, 0x63, 0x6f, 0x6d, 0x2f, 0x75, 0x63,
	0x70, 0x72, 0x2f, 0x77, 0x6f, 0x72, 0x6b, 0x73, 0x70, 0x61, 0x63, 0x65, 0x32, 0x30, 0x32, 0x34,
	0x2f, 0x70, 0x67, 0x67, 0x74, 0x2d, 0x35, 0x31, 0x2f, 0x67, 0x65, 0x6e, 0xa2, 0x02, 0x03, 0x45,
	0x58, 0x58, 0xaa, 0x02, 0x07, 0x45, 0x78, 0x61, 0x6d, 0x70, 0x6c, 0x65, 0xca, 0x02, 0x07, 0x45,
	0x78, 0x61, 0x6d, 0x70, 0x6c, 0x65, 0xe2, 0x02, 0x13, 0x45, 0x78, 0x61, 0x6d, 0x70, 0x6c, 0x65,
	0x5c, 0x47, 0x50, 0x42, 0x4d, 0x65, 0x74, 0x61, 0x64, 0x61, 0x74, 0x61, 0xea, 0x02, 0x07, 0x45,
	0x78, 0x61, 0x6d, 0x70, 0x6c, 0x65, 0x62, 0x06, 0x70, 0x72, 0x6f, 0x74, 0x6f, 0x33,
}

var (
	file_main_proto_rawDescOnce sync.Once
	file_main_proto_rawDescData = file_main_proto_rawDesc
)

func file_main_proto_rawDescGZIP() []byte {
	file_main_proto_rawDescOnce.Do(func() {
		file_main_proto_rawDescData = protoimpl.X.CompressGZIP(file_main_proto_rawDescData)
	})
	return file_main_proto_rawDescData
}

var file_main_proto_msgTypes = make([]protoimpl.MessageInfo, 1)
var file_main_proto_goTypes = []any{
	(*Example)(nil), // 0: example.Example
}
var file_main_proto_depIdxs = []int32{
	0, // [0:0] is the sub-list for method output_type
	0, // [0:0] is the sub-list for method input_type
	0, // [0:0] is the sub-list for extension type_name
	0, // [0:0] is the sub-list for extension extendee
	0, // [0:0] is the sub-list for field type_name
}

func init() { file_main_proto_init() }
func file_main_proto_init() {
	if File_main_proto != nil {
		return
	}
	if !protoimpl.UnsafeEnabled {
		file_main_proto_msgTypes[0].Exporter = func(v any, i int) any {
			switch v := v.(*Example); i {
			case 0:
				return &v.state
			case 1:
				return &v.sizeCache
			case 2:
				return &v.unknownFields
			default:
				return nil
			}
		}
	}
	type x struct{}
	out := protoimpl.TypeBuilder{
		File: protoimpl.DescBuilder{
			GoPackagePath: reflect.TypeOf(x{}).PkgPath(),
			RawDescriptor: file_main_proto_rawDesc,
			NumEnums:      0,
			NumMessages:   1,
			NumExtensions: 0,
			NumServices:   0,
		},
		GoTypes:           file_main_proto_goTypes,
		DependencyIndexes: file_main_proto_depIdxs,
		MessageInfos:      file_main_proto_msgTypes,
	}.Build()
	File_main_proto = out.File
	file_main_proto_rawDesc = nil
	file_main_proto_goTypes = nil
	file_main_proto_depIdxs = nil
}